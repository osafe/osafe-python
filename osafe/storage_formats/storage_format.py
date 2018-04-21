from abc import ABC, abstractproperty, abstractmethod


class StorageFormat(ABC):
    FILENAME = "osafe.enc"

    @abstractproperty
    def exists(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, content):
        pass
