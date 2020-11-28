from datetime import datetime

import pytest
from freezegun import freeze_time

from twitter_cleanup import User


def test_last_status_before_for_user_with_no_status(mocker):
    mocker.patch("twitter_cleanup.user.BotometerResult")
    assert not User().last_status_before()


@freeze_time("2019-12-31")
def test_last_status_before_for_user_with_status(mocker):
    mocker.patch("twitter_cleanup.user.BotometerResult")
    user = User()
    user.status = mocker.MagicMock()
    user.status.created_at = datetime(2019, 12, 25)
    assert user.last_status_before(days=1)
    assert not user.last_status_before(days=30)


def test_user_is_not_bot(mocker):
    botometer_result = mocker.patch("twitter_cleanup.user.BotometerResult").return_value
    botometer_result.probability = 0.001
    user = User.parse(mocker.Mock(), {"protected": False, "id": 123})

    assert not user.is_bot()


def test_user_is_bot(mocker):
    botometer_result = mocker.patch("twitter_cleanup.user.BotometerResult").return_value
    botometer_result.probability = 0.99
    user = User.parse(mocker.Mock(), {"protected": False, "id": 123})

    assert user.is_bot()


def test_user_is_bot_but_protected(mocker):
    botometer_result = mocker.patch("twitter_cleanup.user.BotometerResult").return_value
    botometer_result.probability = 0.99
    user = User.parse(mocker.Mock(), {"protected": True, "id": 123})

    assert not user.is_bot()
