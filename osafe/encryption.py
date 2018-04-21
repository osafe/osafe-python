from Crypto.Cipher import AES
from enum import IntEnum, unique
import hashlib
import secrets


class Encryption:
    class Message:
        @unique
        class Format(IntEnum):
            AES_128 = 1

            @property
            def key_size(self):
                return {
                    self.AES_128: 16
                }[self]

        def __init__(self, format, iv, content):
            self.format = format
            self.iv = iv
            self.content = content

        @property
        def encoded(self):
            return bytes((self.format,)).encode() + self.iv[:self.format.key_size] + self.content

        @classmethod
        def decode(cls, encoded):
            format = cls.Format(ord(encoded[0]))
            return cls(
                format=format,
                iv=encoded[1:format.key_size + 1],
                content=encoded[format.key_size + 1:],
            )

    class Utils:
        @staticmethod
        def generate_key(passphrase):
            return hashlib.sha512(passphrase.encode('utf-8')).digest()

        @staticmethod
        def generate_iv():
            return secrets.token_bytes(64)

        @staticmethod
        def pkcs5_pad(content, format):
            return content + (format.key_size - len(content) % format.key_size) * bytes((format.key_size - len(content) % format.key_size,))

        @staticmethod
        def pkcs5_unpad(content):
            return content[0:-ord(content[-1])]

    def __init__(self, passphrase):
        self.key = self.Utils.generate_key(passphrase)

    def encrypt(self, content):
        format = self.Message.Format.AES_128
        iv = self.Utils.generate_iv()[:format.key_size]
        return self.Message(
            format=format,
            iv=iv,
            content=self._cipher(format, iv).encrypt(
                self.Utils.pkcs5_pad(content.encode('utf-8'), format)
            )
        )

    def decrypt(self, message):
        return self.Utils.pkcs5_unpad(
            self._cipher(message.format, message.iv).decrypt(message.content).decode('utf-8')
        )

    TRANSFORMATIONS = {
        Message.Format.AES_128: AES,
    }

    def _cipher(self, format, iv):
        return self.TRANSFORMATIONS[format].new(
            key=self.key[:format.key_size],
            mode=AES.MODE_CBC,
            IV=iv[:format.key_size],
        )
