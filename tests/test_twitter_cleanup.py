from datetime import datetime

from twitter_cleanup import TwitterCleanup


def test_progress_contains_correct_label(mocker):
    mocker.patch("twitter_cleanup.API")
    mocker.patch("twitter_cleanup.Authentication")
    cleaner = TwitterCleanup()
    progress = cleaner.progress_bar_kwargs("object", 100)
    assert progress["label"] == "Looking for object in 100 accounts"


def test_action_message_is_correctly_formed(mocker):
    mocker.patch("twitter_cleanup.API")
    mocker.patch("twitter_cleanup.Authentication")
    cleaner = TwitterCleanup()

    user = mocker.MagicMock()
    user.screen_name = "MsUser"
    user.status = mocker.MagicMock()
    user.status.created_at = datetime(2019, 12, 2)
    user.status.text = "Hello"

    message = cleaner.action_message("object", user)
    assert "Hello" in message
    assert "MsUser" in message
