from Crypto.Cipher import AES
from cached_property import cached_property
from enum import IntEnum, unique
from io import BytesIO
import hashlib
import secrets


class Encryption:
    class Message:
        @unique
        class Format(IntEnum):
            AES_128_SHA_1 = 1

            @cached_property
            def key_size(self):
                return {
                    self.AES_128_SHA_1: 16,
                }[self]

            @cached_property
            def signer(self):
                return {
                    self.AES_128_SHA_1: hashlib.sha1,
                }[self]

        def __init__(self, format, iv, signature, content):
            self.format = format
            self.iv = iv
            self.signature = signature
            self.content = content

        @property
        def encoded(self):
            return b''.join((
                bytes((self.format,)),
                self.iv,
                self.signature,
                self.content
            ))

        @classmethod
        def decode(cls, encoded):
            stream = BytesIO(encoded)
            format = cls.Format(stream.read(1)[0])

            return cls(
                format=format,
                iv=stream.read(format.key_size),
                signature=stream.read(format.signer().digest_size),
                content=stream.read(),
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
            return content[0:-content[-1]]

    def __init__(self, passphrase):
        self.key = self.Utils.generate_key(passphrase)

    def encrypt(self, content):
        format = self.Message.Format.AES_128_SHA_1
        iv = self.Utils.generate_iv()[:format.key_size]
        content_bytes = content.encode('utf-8')

        return self.Message(
            format=format,
            iv=iv,
            signature=format.signer(content_bytes).digest(),
            content=self._cipher(format, iv).encrypt(
                self.Utils.pkcs5_pad(content_bytes, format)
            )
        )

    def decrypt(self, message):
        content_bytes = self.Utils.pkcs5_unpad(
            self._cipher(message.format, message.iv).decrypt(message.content)
        )
        if message.signature != hashlib.sha1(content_bytes).digest():
            return None

        return content_bytes.decode('utf-8')

    TRANSFORMATIONS = {
        Message.Format.AES_128_SHA_1: AES,
    }

    def _cipher(self, format, iv):
        return self.TRANSFORMATIONS[format].new(
            key=self.key[:format.key_size],
            mode=AES.MODE_CBC,
            IV=iv[:format.key_size],
        )
