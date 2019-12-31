from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock, patch

from twitter_cleanup import User


class UserTest(TestCase):
    @patch("twitter_cleanup.user.BotometerResult")
    @patch("twitter_cleanup.user.datetime")
    def test_last_status_before_for_user_with_no_status(self, dt, bot):
        dt.now.return_value = datetime(2019, 12, 2, 0, 0, 0, 0)
        user = User()
        self.assertFalse(user.last_status_before())

    @patch("twitter_cleanup.user.BotometerResult")
    @patch("twitter_cleanup.user.datetime")
    def test_last_status_before_for_user_with_status(self, dt, bot):
        dt.now.return_value = datetime(2019, 12, 2, 0, 0, 0, 0)
        user = User()
        user.status = Mock()
        user.status.created_at = datetime(2019, 12, 1, 0, 0, 0, 0)
        self.assertTrue(user.last_status_before())
        self.assertFalse(user.last_status_before(hours=48))
