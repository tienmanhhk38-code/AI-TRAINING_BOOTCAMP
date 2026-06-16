import unittest

from frontend.chat_view_model import (
    build_visible_messages,
    get_followup_suggestions,
    get_initial_suggestions,
    next_active_session_id_after_delete,
    normalize_text,
    should_show_empty_state,
)


class ChatViewModelTest(unittest.TestCase):
    def normalized_suggestions(self, suggestions):
        return [normalize_text(suggestion) for suggestion in suggestions]

    def test_appends_pending_user_message_without_mutating_session_messages(self):
        session_messages = [
            {"role": "assistant", "content": "Welcome"},
        ]

        visible_messages = build_visible_messages(session_messages, "Company policy?")

        self.assertEqual(session_messages, [{"role": "assistant", "content": "Welcome"}])
        self.assertEqual(len(visible_messages), 2)
        self.assertEqual(visible_messages[-1]["role"], "user")
        self.assertEqual(visible_messages[-1]["content"], "Company policy?")
        self.assertTrue(visible_messages[-1]["pending"])

    def test_empty_state_hidden_when_pending_question_exists(self):
        self.assertTrue(should_show_empty_state([], None))
        self.assertFalse(should_show_empty_state([], "Company policy?"))

    def test_visible_messages_hide_sources_and_inline_citations(self):
        session_messages = [
            {
                "role": "assistant",
                "content": "CEO is Nguyen Thi Thuy Van [Source: org:c8].",
                "sources": ["org:c8"],
            },
        ]

        visible_messages = build_visible_messages(session_messages, None)

        self.assertNotIn("sources", visible_messages[0])
        self.assertEqual(visible_messages[0]["content"], "CEO is Nguyen Thi Thuy Van.")

    def test_initial_suggestions_are_shown_for_new_chat(self):
        suggestions = get_initial_suggestions()

        self.assertGreaterEqual(len(suggestions), 4)
        self.assertIn("ceo ha noi la ai", self.normalized_suggestions(suggestions))

    def test_followup_suggestions_use_last_user_question_topic(self):
        messages = [
            {"role": "user", "content": "CEO Ha Noi la ai?"},
            {"role": "assistant", "content": "CEO Ha Noi la Nguyen Thi Thuy Van."},
        ]

        suggestions = get_followup_suggestions(messages)

        normalized = self.normalized_suggestions(suggestions)

        self.assertIn("ban dieu hanh bnk gom nhung ai", normalized)
        self.assertIn("vai tro cua ceo bnk hn la gi", normalized)

    def test_followup_suggestions_fall_back_to_general_questions(self):
        suggestions = get_followup_suggestions([
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
        ])

        self.assertIn("cong ty co nhung chinh sach nao", self.normalized_suggestions(suggestions))

    def test_next_active_session_after_delete_keeps_current_when_not_deleted(self):
        sessions = [
            {"id": "one"},
            {"id": "two"},
        ]

        next_session_id = next_active_session_id_after_delete(
            sessions,
            active_session_id="one",
            deleted_session_id="two",
        )

        self.assertEqual(next_session_id, "one")

    def test_next_active_session_after_delete_uses_first_remaining_session(self):
        sessions = [
            {"id": "one"},
            {"id": "two"},
        ]

        next_session_id = next_active_session_id_after_delete(
            sessions,
            active_session_id="two",
            deleted_session_id="two",
        )

        self.assertEqual(next_session_id, "one")

    def test_next_active_session_after_delete_returns_none_when_no_sessions_left(self):
        next_session_id = next_active_session_id_after_delete(
            [],
            active_session_id="one",
            deleted_session_id="one",
        )

        self.assertIsNone(next_session_id)


if __name__ == "__main__":
    unittest.main()
