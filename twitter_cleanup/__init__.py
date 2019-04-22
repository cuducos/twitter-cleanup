import arrow
import click
from tweepy import API, Cursor

from twitter_cleanup.authentication import authentication
from twitter_cleanup.cache import Cache
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
        total = self.me.friends_count
        to_unfollow = []
        cache = Cache("unfollow_inactive_for", kwargs)

        bar_kwargs = dict(
            length=total,
            label=f"Looking for inactive users in {total} accounts",
            width=0,  # 0 means full-width
        )
        with click.progressbar(**bar_kwargs) as bar:
            for user in self.following:
                should_unfollow = cache.get(user.screen_name)

                if should_unfollow is None:  # nothing cached
                    should_unfollow = user.last_status_before(**kwargs)
                    cache.set(user.screen_name, should_unfollow)

                if should_unfollow:
                    to_unfollow.append(user)

                bar.update(1)

        for user in to_unfollow:
            self.unfollow(user)

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
        total = self.me.followers_count
        to_block = []
        cache = Cache("soft_block_bots", threshold)

        bar_kwargs = dict(
            length=total,
            label=f"Looking for bots in {total} accounts",
            width=0,  # 0 means full-width
        )
        with click.progressbar(**bar_kwargs) as bar:
            for user in self.followers:
                should_soft_block = cache.get(user.screen_name)

                if should_soft_block is None:  # nothing cached
                    should_soft_block = user.is_bot()
                    cache.set(user.screen_name, should_soft_block)

                if should_soft_block:
                    to_block.append(user)

                bar.update(1)

        for user in to_block:
            self.soft_block_bot(user)

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
