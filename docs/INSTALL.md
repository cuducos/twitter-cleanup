# Twitter Cleanup<br>the non-developer install guide

The [`README.md`](../README.md) offers instructions for people familiar with the Python developer environment. This guide is an attempt to help non-tech people to use this package.

> Please, let me know where I'm failing and I'll improve this document, ok?

## 1. Install Python 3.6 or newer

Go the the [Python Dowload page](https://www.python.org/downloads/) page and download any version of Python that is 3.6 or newer. Probably the website will point you to the file compatible with your operation system and to the proper instructions.

## 2. Install Twitter Cleanup

Open a terminal (in Windows it might be called _PowerShell_ or _CMD_) and enter the following command (without the dollar sign):

```sh
$ pip install twitter-cleanup
```

If you get an error message saying `pip` is not a valid command, try `python -m ensurepip` first.

## 3. Create the environment variables

Visit Twitter and RapidAPI/Botometer (links are in the [`README.md`](../README.md)) to generate API keys. Then in the directory where you are gonna execute this app you can create a file named `.env` with the following content:

```
TWITTER_CONSUMER_KEY=<Twitter consumer key>
TWITTER_CONSUMER_SECRET=<Twitter consumer secret>
TWITTER_ACCESS_TOKEN_KEY=<Twitter access token key>
TWITTER_ACCESS_TOKEN_SECRET=<Twitter access token secret>
BOTOMETER_MASHAPE_KEY=<Botometer mashape key>
```

Then replace the values between `<` and `>` (including the `<` and `>`) by the keys generated in Twitter and RapidAPI websites.

## 4. Ready!

You're probably ready to go. Follow the usage instructions on [`README.md`](../README.md) from now on.
