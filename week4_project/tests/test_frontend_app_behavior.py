import unittest

from streamlit.testing.v1 import AppTest


class FrontendAppBehaviorTest(unittest.TestCase):
    def run_app(self):
        app = AppTest.from_file("frontend/app.py", default_timeout=20)
        app.run(timeout=20)
        self.assertEqual(len(app.exception), 0)
        return app

    def test_sidebar_does_not_show_clear_current_chat(self):
        app = self.run_app()

        self.assertNotIn("Clear current chat", [button.label for button in app.button])

    def test_delete_session_button_opens_confirmation_dialog(self):
        app = self.run_app()
        delete_buttons = [button for button in app.button if button.label == "x"]
        self.assertTrue(delete_buttons)

        delete_buttons[0].click()
        app.run(timeout=20)

        labels = [button.label for button in app.button]
        self.assertIn("Cancel", labels)
        self.assertIn("Delete chat", labels)


if __name__ == "__main__":
    unittest.main()
