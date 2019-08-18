import os
import json


class Config:
    DEFAULT = {
        'timeout': 5,
    }

    @classmethod
    def get(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        os.makedirs(self.path(), exist_ok=True)

    def path(self, name=None):
        if not name:
            return os.path.expanduser("~/.osafe")
        else:
            return os.path.join(self.path(), name)

    @property
    def content(self):
        if not hasattr(self, '_content'):
            try:
                with open(self.path("config.json")) as f:
                    self._content = json.load(f)
            except FileNotFoundError:
                self._content = {}
        return self._content

    def read(self, name):
        return self.content.get(name, self.DEFAULT[name])

    def write(self, timeout):
        self.content.update(timeout=timeout)
        with open(self.path("config.json"), 'w') as f:
            json.dump(self.content, f)
