from enum import Flag

import backoff
from requests.exceptions import RequestException
from tweepy.error import RateLimitError
from botometer import Botometer, NoTimelineError

from twitter_cleanup.authentication import Authentication


BotometerStatus = Flag("BotometerStatus", "PENDING READY UNAVAILABLE")


class BotometerResultError(Exception):
    pass


class BotometerResult:
    """Holds Botometer result and avoids repeating the request to their API"""

    def __init__(self, user_id=None):
        auth = Authentication.getInstance()
        kwargs = auth.botometer.copy()
        kwargs["wait_on_rate_limit"] = True
        self.botometer = Botometer(**kwargs)

        self.status = BotometerStatus.PENDING
        self._probability = None
        self.user_id = user_id

    def set_user(self, user_id):
        self.user_id = user_id

    @backoff.on_exception(backoff.expo, RateLimitError)
    @backoff.on_exception(backoff.expo, RequestException, max_tries=10)
    def _get_result(self):
        try:
            result = self.botometer.check_account(self.user_id)
        except NoTimelineError:
            self.status = BotometerStatus.UNAVAILABLE
        else:
            self._probability = result.get("cap", {}).get("universal")
            self.status = BotometerStatus.READY

    @property
    def probability(self):
        if not self.user_id:
            raise BotometerResultError("Cannot use Botometer without account ID")

        if self.status is BotometerStatus.PENDING:
            self._get_result()
            return self.probability

        if self.status is BotometerStatus.UNAVAILABLE:
            return 0.0  # let's assume it's not a bot

        return self._probability
