# Twitter Clean-up

Tiny script to clean-up your Twitter account:

* Removing users that have been tweeting for a while
* Soft-blocking bots (blocks and immediately unblocks the account, so it stops following you)

## Translated docs

[PT-BR](./l10n/pt-br.md)

## Requirements

* Python 3.6
* [Twitter API keys](https://apps.twitter.com/) specified in `.env.sample`
* [Botometer API key](https://market.mashape.com/OSoMe/botometer) named `MASHAPE_KEY` in `.env.sample`

## Running

Inside a Python _virtualenv_:

1. Copy `.env.sample` as `.env` and insert your credentials accordingly
1. Install the dependencies with `pip install -r requirements.txt`
1. Start the interactive console with `python -i cleanup.py`

### Removing idle accounts

Call the method `cleanup.unfollow_inactive_for(**kwargs)`.

> It accepts any keyword argument compatible with Python's [`timedelta`](https://docs.python.org/3.6/library/datetime.html#timedelta-objects). **It will prompt you before unfollowing anyone**.

For example, to unfollow users inactive for the last 30 days:

```python
>>> cleanup.unfollow_inactive_for(days=30)
```


### Soft-blocking bots

Call the function `soft_block_bots(threshold=None)`.

> The `threshold` value is a `float` between `0` and `1`. Every public account is analyzed using [Botometer](https://botometer.iuni.iu.edu/#!/) and all acounts with a higher probability than the `threshold` would be considered a bot.  **It will prompt you before soft-blocking anyone**.

For example, to run with the default threshold (`0.75`):

```python
>>> cleanup.soft_block_bots()
```

Or to run with a custom threshold:

```python
>>> cleanup.soft_block_bots(threshold=0.68)
```

## Contributing

Please, format your code with [Black](https://github.com/ambv/black).
