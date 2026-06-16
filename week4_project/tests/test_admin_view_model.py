import unittest

from frontend.admin_view_model import build_document_rows, filter_documents, normalize_uploaded_files


class AdminViewModelTest(unittest.TestCase):
    def test_normalize_uploaded_files_accepts_single_file_or_list(self):
        single_file = object()
        file_list = [object(), object()]

        self.assertEqual(normalize_uploaded_files(None), [])
        self.assertEqual(normalize_uploaded_files(single_file), [single_file])
        self.assertEqual(normalize_uploaded_files(file_list), file_list)

    def test_build_document_rows_uses_safe_defaults(self):
        rows = build_document_rows([
            {
                "id": "abcdef123456",
                "filename": "policy.pdf",
                "status": "approved",
                "chunk_count": 3,
                "policy_score": 82,
                "updated_at": "2026-06-16T07:00:00+00:00",
            },
            {
                "id": "xyz",
                "filename": "unknown.txt",
            },
        ])

        self.assertEqual(rows[0]["id"], "abcdef123456")
        self.assertEqual(rows[0]["short_id"], "abcdef12")
        self.assertEqual(rows[0]["filename"], "policy.pdf")
        self.assertEqual(rows[0]["status"], "approved")
        self.assertEqual(rows[0]["chunks"], 3)
        self.assertEqual(rows[0]["score"], 82)
        self.assertEqual(rows[1]["status"], "unknown")
        self.assertEqual(rows[1]["chunks"], 0)

    def test_filter_documents_by_status_and_text(self):
        documents = [
            {"filename": "Leave Policy.pdf", "status": "approved", "matched_keywords": ["policy"]},
            {"filename": "Recipe.docx", "status": "needs_review", "matched_keywords": []},
        ]

        approved = filter_documents(documents, status_filter="approved", search_text="")
        searched = filter_documents(documents, status_filter="All", search_text="leave")

        self.assertEqual([document["filename"] for document in approved], ["Leave Policy.pdf"])
        self.assertEqual([document["filename"] for document in searched], ["Leave Policy.pdf"])


if __name__ == "__main__":
    unittest.main()
