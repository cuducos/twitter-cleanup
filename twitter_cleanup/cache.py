import os.path
from datetime import datetime, timedelta
from pathlib import Path
from pickle import UnpicklingError, dump, load


class Cache:
    def __init__(self, called_by, caller_args, expires_in=7):
        self.expires_in = expires_in  # days
        self.called_by = called_by
        self.caller_args = caller_args
        file_name = f".twitter-cleanup.cache.{called_by}"
        self.cache = Path(os.path.expanduser("~")) / file_name

        if not self.cache.exists():
            self._create()

        if not self.is_valid():
            self.cache.unlink()
            self._create()

    def is_valid(self):
        assert self.cache.is_file()
        with open(self.cache, "rb") as fobj:
            try:
                data = load(fobj)
            except (UnpicklingError, EOFError):
                return False

            if not self.is_valid_data(data):
                return False

            limit = datetime.now() - timedelta(days=self.expires_in)
            expired = data["created_at"] <= limit
            if expired:
                return False

            return True

    def is_valid_data(self, data):
        keys = {"called_by", "caller_args", "created_at", "usernames"}
        if keys != data.keys():
            return False

        if data["called_by"] != self.called_by:
            return False

        if data["caller_args"] != self.caller_args:
            return False

        if not isinstance(data["created_at"], datetime):
            return False

        if data["usernames"]:
            for username, cached_user_data in data["usernames"].items():
                if not isinstance(username, str):
                    return False
                if not isinstance(cached_user_data, bool):
                    return False

        return True

    def _create(self):
        initial_data = {
            "called_by": self.called_by,
            "caller_args": self.caller_args,
            "created_at": datetime.now(),
            "usernames": dict(),
        }
        self._save(initial_data)

    def _read(self):
        assert self.is_valid()
        with open(self.cache, "rb") as fobj:
            data = load(fobj)
        return data

    def _save(self, data):
        assert self.is_valid_data(data)
        with open(self.cache, "wb") as fobj:
            dump(data, fobj)

    def set(self, username, cached_user_data):
        assert isinstance(cached_user_data, bool)
        data = self._read()
        assert self.is_valid_data(data)
        data["usernames"][username] = cached_user_data
        self._save(data)

    def get(self, username):
        data = self._read()
        return data["usernames"].get(username)

    def unset(self, username):
        data = self._read()
        if username in data["usernames"]:
            del data["usernames"][username]
        self._save(data)
