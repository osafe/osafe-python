from getpass import getpass
from subprocess import Popen, TimeoutExpired
from tempfile import NamedTemporaryFile
import os

from .encryption import Encryption
from .storage import Storage
from .config import Config


class Editor:
    def __init__(self):
        self.storage = Storage()

    def start(self):
        self.decrypt()
        self.edit()

    def decrypt(self):
        message = self.storage.get()
        self.content = None

        while self.content is None:
            if message:
                passphrase = getpass("Enter your passphrase: ")
            else:
                passphrase = None
                passphrase_confirmation = None
                while not passphrase or passphrase != passphrase_confirmation:
                    passphrase = getpass("Enter your new passphrase: ")
                    passphrase_confirmation = getpass("Enter the same passphrase again: ")

            self.encryption = Encryption(passphrase)

            if message:
                self.content = self.encryption.decrypt(message)
            else:
                self.content = ""

    def edit(self):
        with NamedTemporaryFile(prefix="osafe-", mode='w+t', encoding='utf-8', newline='\n') as file:
            file.write(self.content)
            file.seek(0)

            editor = os.environ.get('EDITOR')
            if not editor:
                print("EDITOR environment variable not set.")
                while not editor:
                    editor = input("Type your preferred editor: ")

            process = Popen([editor, file.name])
            try:
                process.wait(Config.get().read('timeout') * 60 or None)
            except TimeoutExpired:
                process.kill()
                process.wait()
                self.clear()
                print("Editor timed out, killing and storing last saved content")

            new_content = file.read()
            if new_content != self.content:
                self.storage.set(self.encryption.encrypt(new_content))

    def clear(self):
        if os.name != 'nt':
            os.system('reset')
            os.system('clear')
        else:
            os.system('cls')
