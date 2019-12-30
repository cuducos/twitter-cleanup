
from unittest import TestCase, mock
import datetime

import twitter_cleanup


class UserTest(TestCase):

    @mock.patch('twitter_cleanup.user.BotometerResult')
    @mock.patch('twitter_cleanup.user.datetime')
    def test_last_status_before(self, dt, bot):
        dt.now.return_value = datetime.datetime(2019, 12, 2, 0, 0, 0, 0)
        user = twitter_cleanup.User()
        self.assertFalse(user.last_status_before())

        user.status = mock.Mock()
        user.status.created_at = datetime.datetime(2019, 12, 1, 0, 0, 0, 0)
        self.assertTrue(user.last_status_before())

        self.assertFalse(user.last_status_before(hours=48))
