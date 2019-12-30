from unittest import TestCase, mock
import datetime

import twitter_cleanup


class TwitterCleanupTest(TestCase):
    @mock.patch("twitter_cleanup.API")
    @mock.patch("twitter_cleanup.Authentication")
    def test_progress(self, mock_auth, api_mock):
        cleaner = twitter_cleanup.TwitterCleanup()
        progress = cleaner.progress_bar_kwargs("object", 100)
        self.assertEqual(progress["label"], "Looking for object in 100 accounts")

    @mock.patch("twitter_cleanup.API")
    @mock.patch("twitter_cleanup.Authentication")
    def test_action_message(self, mock_auth, api_mock):
        cleaner = twitter_cleanup.TwitterCleanup()
        mock_user = mock.Mock(
            status=mock.Mock(created_at=datetime.datetime(2019, 12, 2, 0, 0, 0, 0))
        )
        mock_user.status.text = "Hello"
        mock_user.screen_name = "MrUser"
        message = cleaner.action_message("object", mock_user)
        self.assertIn("Hello", message)
        self.assertIn("MrUser", message)
