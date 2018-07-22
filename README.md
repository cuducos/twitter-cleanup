# Twitter Clean-up

> [🇧🇷 Versão em português do Brasil](docs/README.pt-BR.md)

Tiny script to clean-up your Twitter account:

* Removing users that have not been tweeting for a while
* Soft-blocking bots (blocks and immediately unblocks the account, so it stops following you)

## Requirements

* Python 3.6
* [Twitter API keys](https://apps.twitter.com/) specified in `.env.sample`
* [Botometer API key](https://market.mashape.com/OSoMe/botometer) named `MASHAPE_KEY` in `.env.sample`

## Running

Inside a Python _virtualenv_:

1. Copy `.env.sample` as `.env` and insert your credentials accordingly
1. Install the dependencies with `pip install -r requirements.txt`
1. Run the CLI with `python -m twitter_cleanup` and follow the instructions

## Contributing

Please, format your code with [Black](https://github.com/ambv/black).
