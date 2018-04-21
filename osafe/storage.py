from .encryption import Encryption
from .storage_formats.drive_storage_format import DriveStorageFormat


class Storage:
    def __init__(self):
        self.storage_format = DriveStorageFormat()

    @property
    def exists(self):
        return self.storage_format.exists

    def get(self):
        content = self.storage_format.read()
        if content:
            return Encryption.Message.decode(content)

    def set(self, message):
        self.storage_format.write(message.encoded)

    def reset(self):
        self.storage_format.reset()
