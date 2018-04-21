from .encryption import Encryption
from .storage_formats.drive_storage_format import DriveStorageFormat


class Storage:
    def __init__(self):
        self.storage_format = DriveStorageFormat()

    def get(self):
        return Encryption.Message.decode(self.storage_format.read())

    def set(self, message):
        self.storage_format.set(message.encoded)
