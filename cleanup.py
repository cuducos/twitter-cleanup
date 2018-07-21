from datetime import datetime, timedelta

import arrow
from botometer import Botometer
from decouple import config
from tweepy import API, Cursor, OAuthHandler, models


class Authentication:
    """Holds authentication data for further usage in the script"""

    def __init__(self):
        self.consumer_key = config("CONSUMER_KEY")
        self.consumer_secret = config("CONSUMER_SECRET")
        self.access_token = config("ACCESS_TOKEN_KEY")
        self.access_token_secret = config("ACCESS_TOKEN_SECRET")
        self.mashape_key = config("MASHAPE_KEY", default=None)

    @property
    def tweepy(self):
        """Returns an authentication object required by Tweepy"""
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        return auth

    @property
    def botometer(self):
        """Returns a dictionary compatible with Botometer API"""
        return dict(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
            mashape_key=self.mashape_key,
        )


class User(models.User):
    """A wrapper for Tweepy native User model, including custom methods to
    check idle accounts and bots"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        authentication = Authentication()
        self.botometer = Botometer(wait_on_ratelimit=True, **authentication.botometer)
        self._botometer_result = None

    @classmethod
    def parse(cls, api, data):
        """This is how Tweepy instantiate User models from the API result"""
        return super(User, cls).parse(api, data)

    def last_status_before(self, **kwargs):
        """Takes any kwarg compatible with Python's `timedelta` and says
        whether the user's last tweet is older than the `timedelta` defined by
        these kwargs"""
        if not self.status:
            return False

        return self.status.created_at < datetime.now() - timedelta(**kwargs)

    @property
    def botometer_result(self):
        if self._botometer_result:
            return self._botometer_result

        result = self.botometer.check_account(self.id)
        self._botometer_result = result.get("cap", {}).get("universal")
        return self.botometer_result

    def is_bot(self, threshold=0.75):
        if self.protected or not self.botometer_result:
            return False

        return self.botometer_result > threshold


class Cleanup:
    """Core class of this module, holding the methods to clean up the
    authenticated Twitter account."""

    def __init__(self):
        self.authentication = Authentication()
        self.api = API(self.authentication.tweepy)
        self.me = self.api.me()

    @property
    def following(self):
        """Generator with all accounts following the authenticated user"""
        for users in Cursor(self.api.friends).pages():
            yield from (User.parse(self.api, user._json) for user in users)

    @property
    def followers(self):
        """Generator with all accounts followed by the authenticated user"""
        for users in Cursor(self.api.followers).pages():
            yield from (User.parse(self.api, user._json) for user in users)

    def unfollow_inactive_for(self, **kwargs):
        """Takes any kwarg compatible with Python's `timedelta` and unfollows
        users whose last tweet are older than the `timedelta` defined by these
        kwargs"""
        total, count = self.me.friends_count, 0
        for user in self.following:
            if user.last_status_before(**kwargs):
                self.unfollow(user)
            count += 1
            self.percent(count, total)

    def unfollow(self, user):
        """Confirms and unfollow a given user"""
        last_tweet_date = arrow.get(user.status.created_at)
        message = (
            f"Confirm unfollow {user.screen_name}?\n\n"
            f"Last tweet was {last_tweet_date.humanize()}:\n\n"
            f"{user.status.text}\n\n"
        )
        if not self.confirm(message):
            return

        self.api.destroy_friendship(user.id)
        print(f"Unfollowed {user.screen_name}")

    def soft_block_bots(self, threshold=None):
        """Soft-blocks every bot account classified by Botometer lower than the
        `threshold` (defaults to 0.75 in User class)."""
        total, count = self.me.followers_count, 0
        for user in self.followers:
            if user.is_bot():
                self.soft_block_bot(user)
            count += 1
            self.percent(count, total)

    def soft_block_bot(self, user):
        """Confirms and soft-block a given account"""
        message = (
            f"Confirm soft-block {user.screen_name}?\n"
            f"{100 * user.botometer_result:.2f}% probability of being a bot"
        )
        if not self.confirm(message):
            return

        self.api.create_block(user.id)
        self.api.destroy_block(user.id)
        print(f"Soft-blocked {user.screen_name}?")

    @staticmethod
    def confirm(message):
        result = input(f"{message}\n[y/n] ")
        return result.lower() == "y"

    @staticmethod
    def percent(count, total):
        percent = count / total
        message = f"[{100 *percent:.2f}%] {count} out of {total} accounts"
        print(message, end="\r")


if __name__ == "__main__":
    cleanup = Cleanup()
