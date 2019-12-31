# Twitter Clean-up [![GitHub Actions: Black workflow](https://github.com/cuducos/twitter-cleanup/workflows/Black/badge.svg)]()

> [🇧🇷 Versão em português do Brasil](docs/README.pt-BR.md)

Tiny script to clean-up your Twitter account:

* Removing users that have not been tweeting for a while
* Soft-blocking bots (blocks and immediately unblocks the account, so it stops following you)

## Requirements


* Python 3.6+
* Set environment variables with your [Twitter API keys](https://apps.twitter.com/) and with [Botometer API key](https://rapidapi.com/OSoMe/api/botometer):
    * `TWITTER_CONSUMER_KEY`
    * `TWITTER_CONSUMER_SECRET`
    * `TWITTER_ACCESS_TOKEN_KEY`
    * `TWITTER_ACCESS_TOKEN_SECRET`
    * `BOTOMETER_MASHAPE_KEY`

## Installing


Install the package with:

```console
$ pip install twitter-cleanup
```

Usage
-----

Run the CLI with `twitter-cleanup --help` and follow the on screen instructions.

For example, unfollow everyone that hasn't tweeted in the last 30 days with:

```console
$ twitter-cleanup inactive 30
```

Or soft-block every bot with:

```
$ twitter-cleanup bots
```

Contributing
------------

Please, format your code with [Black](https://github.com/ambv/black>).
Also, it's a great idea to run the unit tests locally, using [Pytest](http://doc.pytest.org>) or your IDE test runner.
