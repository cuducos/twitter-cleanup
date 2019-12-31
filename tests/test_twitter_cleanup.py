from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock, patch

from twitter_cleanup import TwitterCleanup


class TwitterCleanupTest(TestCase):
    @patch("twitter_cleanup.API")
    @patch("twitter_cleanup.Authentication")
    def test_progress_contains_correct_label(self, mock_auth, api_mock):
        cleaner = TwitterCleanup()
        progress = cleaner.progress_bar_kwargs("object", 100)
        self.assertEqual(progress["label"], "Looking for object in 100 accounts")

    @patch("twitter_cleanup.API")
    @patch("twitter_cleanup.Authentication")
    def test_action_message_is_correctly_formed(self, mock_auth, api_mock):
        cleaner = TwitterCleanup()
        mock_user = Mock()
        mock_user.status = Mock()
        mock_user.status.created_at = datetime(2019, 12, 2, 0, 0, 0, 0)
        mock_user.status.text = "Hello"
        mock_user.screen_name = "MrUser"
        message = cleaner.action_message("object", mock_user)
        self.assertIn("Hello", message)
        self.assertIn("MrUser", message)
