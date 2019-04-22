from datetime import datetime, timedelta

from tweepy import models

from twitter_cleanup.botometer import BotometerResult


class User(models.User):
    """A wrapper for Tweepy native User model, including custom methods to
    check idle accounts and bots"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.botometer_result = BotometerResult()

    @classmethod
    def parse(cls, api, data):
        """This is how Tweepy instantiate User models from the API result"""
        return super(User, cls).parse(api, data)

    def last_status_before(self, **kwargs):
        """Takes any kwarg compatible with Python's `timedelta` and says
        whether the user's last tweet is older than the `timedelta` defined by
        these kwargs"""
        if not getattr(self, "status", None):
            return False

        return self.status.created_at < datetime.now() - timedelta(**kwargs)

    def is_bot(self, threshold=0.75):
        if self.protected:
            return False

        self.botometer_result.set_user(self.id)
        return self.botometer_result.probability > threshold
