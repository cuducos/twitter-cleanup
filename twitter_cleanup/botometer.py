from enum import Flag

from botometer import Botometer, NoTimelineError

from twitter_cleanup.authentication import authentication


BotometerStatus = Flag("BotometerStatus", "PENDING READY UNAVAILABLE")


class BotometerResultError(Exception):
    pass


class BotometerResult:
    """Holds Botometer result and avoids repeating the request to their API"""

    def __init__(self, user_id=None):
        kwargs = authentication.botometer.copy()
        kwargs["wait_on_rate_limit"] = True
        self.botometer = Botometer(**kwargs)

        self.status = BotometerStatus.PENDING
        self._probability = None
        self.user_id = user_id

    def set_user(self, user_id):
        self.user_id = user_id

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
