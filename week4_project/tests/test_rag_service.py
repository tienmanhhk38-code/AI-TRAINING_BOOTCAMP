import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from backend import gemini_client as gemini_client_module
from backend.chat_store import ChatSessionStore
from backend.chroma_store import ChromaStore
from backend.document_loader import load_document_text
from backend.document_policy import classify_document
from backend.gemini_client import GeminiClient
from backend.rag_service import RAGService, chunk_text

class RAGServiceTest(unittest.TestCase):
    def test_chunk_text_creates_chunks_with_sources(self):
        chunks = chunk_text("hello world " * 80, source="sample.txt", chunk_size=100, overlap=10)

        self.assertGreater(len(chunks), 1)
        self.assertEqual(chunks[0]["source"], "sample.txt")
        self.assertTrue(chunks[0]["chunk_id"].startswith("sample.txt:c"))

    def test_retrieve_returns_expected_source(self):
        service = RAGService([
            {
                "chunk_id": "week2:c1",
                "source": "week2",
                "text": "Week 2 teaches OCR and PDF processing.",
            },
            {
                "chunk_id": "week4:c1",
                "source": "week4",
                "text": "Week 4 builds FastAPI backend and Streamlit UI.",
            },
        ])

        result = service.ask("Which week teaches OCR?")

        self.assertEqual(result["sources"][0], "week2:c1")
        self.assertIn("OCR", result["answer"])

    def test_retrieve_handles_vietnamese_branch_role_question(self):
        service = RAGService([
            {
                "chunk_id": "org:c1",
                "source": "org.pdf",
                "text": (
                    "Organization Chart BnK HN Dia diem kinh doanh "
                    "CEO HDQT Executive Board CEO CEO CEO"
                ),
            },
            {
                "chunk_id": "org:c8",
                "source": "org.pdf",
                "text": (
                    "Effective date January 1st 2025. "
                    "Mrs. NGUYEN THI THUY VAN. "
                    "Appointment Mrs. NGUYEN THI THUY VAN to the position of: "
                    "CEO of BnK HN. Director of APO."
                ),
            },
        ])

        results = service.retrieve("CEO hà nội là ai?", top_k=1)

        self.assertEqual(results[0]["chunk_id"], "org:c8")

    def test_empty_question_returns_error_answer(self):
        service = RAGService([])

        result = service.ask("   ")

        self.assertEqual(result["answer"], "Question is empty.")
        self.assertEqual(result["sources"], [])

    def test_llm_client_is_used_when_configured(self):
        class FakeLLMClient:
            def generate_answer(self, question, contexts, **kwargs):
                return f"LLM answer for {question} from {contexts[0]['chunk_id']}"

        service = RAGService(
            [
                {
                    "chunk_id": "week4:c1",
                    "source": "week4",
                    "text": "Week 4 builds FastAPI backend and Streamlit UI.",
                },
            ],
            llm_client=FakeLLMClient(),
        )

        result = service.ask("What does Week 4 build?")

        self.assertEqual(result["llm"], "gemini")
        self.assertIn("LLM answer", result["answer"])
        self.assertEqual(result["sources"], ["week4:c1"])

    def test_document_answer_hides_source_citations_from_user_text(self):
        class FakeLLMClient:
            def generate_answer(self, question, contexts, **kwargs):
                return "CEO is Nguyen Thi Thuy Van [Source: org:c8]."

        service = RAGService(
            [
                {
                    "chunk_id": "org:c8",
                    "source": "org.pdf",
                    "text": "Mrs. Nguyen Thi Thuy Van is CEO of BnK HN.",
                },
            ],
            llm_client=FakeLLMClient(),
        )

        result = service.ask("CEO BnK HN la ai?")

        self.assertEqual(result["answer"], "CEO is Nguyen Thi Thuy Van.")
        self.assertEqual(result["sources"], ["org:c8"])

    def test_vector_store_is_used_when_configured(self):
        class FakeVectorStore:
            def reset(self, chunks):
                self.chunks = chunks

            def query(self, question, top_k=3):
                return [
                    {
                        "chunk_id": "vector:c1",
                        "source": "vector",
                        "text": "Vector DB retrieved this context.",
                        "score": 0.99,
                    }
                ]

        service = RAGService(
            [
                {
                    "chunk_id": "local:c1",
                    "source": "local",
                    "text": "Local context should not win.",
                },
            ],
            vector_store=FakeVectorStore(),
        )

        result = service.ask("anything")

        self.assertEqual(result["sources"], ["vector:c1"])
        self.assertIn("Vector DB", result["answer"])

    def test_chroma_store_accepts_duplicate_chunk_ids(self):
        chunks = [
            {
                "chunk_id": "same:c1",
                "source": "same.txt",
                "text": "First chunk about FastAPI.",
            },
            {
                "chunk_id": "same:c1",
                "source": "same.txt",
                "text": "Second chunk about ChromaDB.",
            },
        ]

        with TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
            store = ChromaStore(Path(temp_dir), collection_name="duplicate_id_test")
            try:
                store.reset(chunks)
                results = store.query("Which chunk mentions ChromaDB?", top_k=2)
            finally:
                store.close()

        self.assertTrue(results)
        self.assertIn("same:c1", [result["chunk_id"] for result in results])

    def test_document_policy_marks_company_doc_approved(self):
        result = classify_document(
            "bnk_policy.txt",
            "BNK company policy covers nghi phep and phuc loi.",
        )

        self.assertEqual(result["status"], "approved")
        self.assertIn("bnk", result["matched_keywords"])

    def test_document_policy_marks_unrelated_doc_needs_review(self):
        result = classify_document(
            "recipe.txt",
            "This document explains pasta recipes and tomato sauce.",
        )

        self.assertEqual(result["status"], "needs_review")

    def test_load_csv_document_text(self):
        text = load_document_text(
            "policy.csv",
            "name,value\npolicy,BNK leave policy\n".encode("utf-8"),
        )

        self.assertIn("policy | BNK leave policy", text)

    def test_general_question_uses_gemini_without_context(self):
        class FakeLLMClient:
            def generate_general_answer(self, question, **kwargs):
                return f"General answer: {question}"

        service = RAGService([], llm_client=FakeLLMClient())

        result = service.ask("What is Python?")

        self.assertEqual(result["llm"], "gemini_general")
        self.assertIn("General answer", result["answer"])

    def test_general_question_passes_history_and_current_date_to_gemini(self):
        class FakeLLMClient:
            def __init__(self):
                self.history = None
                self.current_date = None

            def generate_general_answer(self, question, history=None, current_date=None):
                self.history = history
                self.current_date = current_date
                return "context-aware answer"

        llm_client = FakeLLMClient()
        service = RAGService([], llm_client=llm_client)
        history = [
            {"role": "user", "content": "lich thi dau wc 2026"},
            {"role": "assistant", "content": "FIFA World Cup 2026 schedule"},
        ]

        result = service.ask("la?", history=history, current_date="Tuesday, June 16, 2026")

        self.assertEqual(result["llm"], "gemini_general")
        self.assertEqual(llm_client.history, history)
        self.assertEqual(llm_client.current_date, "Tuesday, June 16, 2026")

    def test_document_answer_passes_history_and_current_date_to_gemini(self):
        class FakeLLMClient:
            def __init__(self):
                self.history = None
                self.current_date = None

            def generate_answer(self, question, contexts, history=None, current_date=None):
                self.history = history
                self.current_date = current_date
                return "document answer"

        llm_client = FakeLLMClient()
        service = RAGService(
            [
                {
                    "chunk_id": "policy:c1",
                    "source": "policy",
                    "text": "BNK policy allows annual leave.",
                },
            ],
            llm_client=llm_client,
        )
        history = [{"role": "user", "content": "BNK policy?"}]

        result = service.ask("annual leave?", history=history, current_date="Tuesday, June 16, 2026")

        self.assertEqual(result["llm"], "gemini")
        self.assertEqual(llm_client.history, history)
        self.assertEqual(llm_client.current_date, "Tuesday, June 16, 2026")

    def test_gemini_prompt_uses_history_current_date_and_larger_output_budget(self):
        captured = {}

        class FakeResponse:
            def raise_for_status(self):
                return None

            def json(self):
                return {
                    "candidates": [
                        {
                            "content": {
                                "parts": [{"text": "answer"}],
                            },
                        },
                    ],
                }

        def fake_post(url, headers, json, timeout):
            captured["json"] = json
            return FakeResponse()

        original_post = gemini_client_module.requests.post
        try:
            gemini_client_module.requests.post = fake_post
            client = GeminiClient("fake-key")
            client.generate_general_answer(
                "la?",
                history=[
                    {"role": "user", "content": "lich thi dau wc 2026"},
                    {"role": "assistant", "content": "FIFA World Cup 2026 schedule"},
                ],
                current_date="Tuesday, June 16, 2026",
            )
        finally:
            gemini_client_module.requests.post = original_post

        prompt = captured["json"]["contents"][0]["parts"][0]["text"]
        self.assertIn("Current date: Tuesday, June 16, 2026", prompt)
        self.assertIn("user: lich thi dau wc 2026", prompt)
        self.assertIn("assistant: FIFA World Cup 2026 schedule", prompt)
        self.assertNotIn("Keep the answer concise", prompt)
        self.assertGreaterEqual(captured["json"]["generationConfig"]["maxOutputTokens"], 2048)

    def test_greeting_uses_local_answer_without_gemini(self):
        class FailingLLMClient:
            def generate_general_answer(self, question, **kwargs):
                raise TimeoutError("should not be called")

        service = RAGService([], llm_client=FailingLLMClient())

        result = service.ask("hi")

        self.assertEqual(result["llm"], "local_greeting")
        self.assertIn("Bnk Chatbot", result["answer"])

    def test_identity_question_uses_local_answer_without_gemini(self):
        class FailingLLMClient:
            def generate_general_answer(self, question):
                raise TimeoutError("should not be called")

        service = RAGService([], llm_client=FailingLLMClient())

        vietnamese_result = service.ask("bạn là ai")
        english_result = service.ask("who are you")

        self.assertEqual(vietnamese_result["llm"], "local_identity")
        self.assertEqual(english_result["llm"], "local_identity")
        self.assertIn("Bnk Chatbot", vietnamese_result["answer"])

    def test_gemini_timeout_returns_friendly_fallback(self):
        class TimeoutLLMClient:
            def generate_general_answer(self, question, **kwargs):
                raise TimeoutError("ReadTimeout")

        service = RAGService([], llm_client=TimeoutLLMClient())

        result = service.ask("What is Python?")

        self.assertEqual(result["llm"], "local_fallback")
        self.assertIn("Gemini is not responding", result["answer"])
        self.assertNotIn("Gemini failed with", result["answer"])
        self.assertNotIn("ReadTimeout", result["answer"])

    def test_company_question_without_context_does_not_hallucinate(self):
        class FakeLLMClient:
            def generate_general_answer(self, question, **kwargs):
                return f"General answer: {question}"

        service = RAGService([], llm_client=FakeLLMClient())

        result = service.ask("What is BNK leave policy?")

        self.assertEqual(result["llm"], "gemini_no_context")
        self.assertEqual(result["sources"], [])

    def test_gemini_blank_timeout_uses_default(self):
        import os

        old_key = os.environ.get("GEMINI_API_KEY")
        old_timeout = os.environ.get("GEMINI_TIMEOUT_SECONDS")
        try:
            os.environ["GEMINI_API_KEY"] = "fake-key"
            os.environ["GEMINI_TIMEOUT_SECONDS"] = ""

            client = GeminiClient.from_env()

            self.assertEqual(client.timeout, GeminiClient.DEFAULT_TIMEOUT)
        finally:
            if old_key is None:
                os.environ.pop("GEMINI_API_KEY", None)
            else:
                os.environ["GEMINI_API_KEY"] = old_key
            if old_timeout is None:
                os.environ.pop("GEMINI_TIMEOUT_SECONDS", None)
            else:
                os.environ["GEMINI_TIMEOUT_SECONDS"] = old_timeout

    def test_chat_session_store_persists_sessions(self):
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "chat_sessions.json"
            store = ChatSessionStore(path)
            session = store.create("New chat")
            answer = {
                "answer": "Hello from Bnk Chatbot",
                "sources": [],
                "llm": "local",
            }

            updated = store.add_exchange(session["id"], "hello", answer)
            reloaded = ChatSessionStore(path).get(session["id"])

            self.assertEqual(updated["title"], "hello")
            self.assertEqual(len(reloaded["messages"]), 2)
            self.assertEqual(reloaded["messages"][0]["role"], "user")
            self.assertEqual(reloaded["messages"][1]["role"], "assistant")

            cleared = store.clear(session["id"])

            self.assertEqual(cleared["messages"], [])

if __name__ == "__main__":
    unittest.main()
