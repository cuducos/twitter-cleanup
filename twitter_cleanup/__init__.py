import arrow
import click
from tweepy import API, Cursor

from twitter_cleanup.authentication import authentication
from twitter_cleanup.user import User


class TwitterCleanup:
    """Core class of this package, holding the methods to clean up the
    authenticated Twitter account."""

    def __init__(self, assume_yes=False):
        self.api = API(authentication.tweepy, wait_on_rate_limit=True)
        self.me = self.api.me()
        self.assume_yes = assume_yes

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
        click.echo(f"Unfollowed {user.screen_name}")

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
        percent = 100 * user.botometer_result.probability
        message = (
            f"Confirm soft-block {user.screen_name}?\n"
            f"{percent:.2f}% probability of being a bot"
        )
        if not self.confirm(message):
            return

        self.api.create_block(user.id)
        self.api.destroy_block(user.id)
        click.echo(f"Soft-blocked {user.screen_name}")

    def confirm(self, message):
        if self.assume_yes:
            return True

        return click.confirm(message)

    @staticmethod
    def percent(count, total):
        percent = (count * 100) / total
        message = f"[{percent:.2f}%] {count} out of {total} accounts"
        print(message, end="\r")
