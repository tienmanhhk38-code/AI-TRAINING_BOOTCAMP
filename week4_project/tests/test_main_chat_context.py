import unittest

from backend import main as main_module


class MainChatContextTest(unittest.TestCase):
    def test_ask_passes_session_history_to_rag_service(self):
        captured = {}

        class FakeRAGService:
            def ask(self, question, history=None, current_date=None):
                captured["question"] = question
                captured["history"] = history
                captured["current_date"] = current_date
                return {
                    "answer": "answer",
                    "sources": [],
                    "contexts": [],
                    "llm": "gemini_general",
                }

        class FakeChatSessionStore:
            def get(self, session_id):
                return {
                    "id": session_id,
                    "title": "Existing chat",
                    "messages": [
                        {"role": "user", "content": "lich thi dau wc 2026"},
                        {"role": "assistant", "content": "World Cup 2026 schedule"},
                    ],
                }

            def add_exchange(self, session_id, question, answer_record):
                return {"id": session_id, "title": "Existing chat"}

        original_rag_service = main_module.rag_service
        original_chat_session_store = main_module.chat_session_store
        original_append_conversation = main_module.append_conversation
        try:
            main_module.rag_service = FakeRAGService()
            main_module.chat_session_store = FakeChatSessionStore()
            main_module.append_conversation = lambda path, question, answer: None

            result = main_module.ask(main_module.AskRequest(question="la?", session_id="session-1"))
        finally:
            main_module.rag_service = original_rag_service
            main_module.chat_session_store = original_chat_session_store
            main_module.append_conversation = original_append_conversation

        self.assertEqual(result["session_id"], "session-1")
        self.assertEqual(captured["question"], "la?")
        self.assertEqual(captured["history"][0]["content"], "lich thi dau wc 2026")
        self.assertIn("20", captured["current_date"])


if __name__ == "__main__":
    unittest.main()
