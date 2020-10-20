import os
from pathlib import Path

from click.testing import CliRunner

from twitter_cleanup.__main__ import cli


def test_command_bots(mocker):
    cleaner = mocker.patch("twitter_cleanup.__main__.TwitterCleanup").return_value
    runner = CliRunner()
    result = runner.invoke(cli, ["bots"])
    assert result.exit_code == 0
    cleaner.soft_block_bots.assert_called_once()


def test_command_bots_with_wrong_too_high_argument(mocker):
    mocker.patch("twitter_cleanup.__main__.TwitterCleanup")
    runner = CliRunner()
    result = runner.invoke(cli, ["bots", "101"])
    assert result.exit_code == 2


def test_command_bots_with_wrong_too_low_argument(mocker):
    mocker.patch("twitter_cleanup.__main__.TwitterCleanup")
    runner = CliRunner()
    result = runner.invoke(cli, ["bots", "-1"])
    assert result.exit_code == 2


def test_command_inactive(mocker):
    cleaner = mocker.patch("twitter_cleanup.__main__.TwitterCleanup").return_value
    runner = CliRunner()
    result = runner.invoke(cli, ["inactive", "123"])
    assert result.exit_code == 0
    cleaner.unfollow_inactive_for.assert_called_once_with(days=123)


def test_command_clear_cache(mocker):
    mocker.patch("twitter_cleanup.__main__.TwitterCleanup")
    path = mocker.patch("twitter_cleanup.__main__.Path").return_value
    file = mocker.Mock()
    path.glob.return_value = [file]
    runner = CliRunner()
    result = runner.invoke(cli, ["clear-cache"])
    assert result.exit_code == 0
    file.unlink.assert_called_once()

    file2 = mocker.Mock()
    path.glob.return_value = [file2, file2, file2]
    runner.invoke(cli, ["clear-cache"])
    assert 3 == file2.unlink.call_count
