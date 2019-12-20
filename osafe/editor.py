from contextlib import contextmanager
from getpass import getpass
from subprocess import Popen, TimeoutExpired
from tempfile import NamedTemporaryFile
from threading import Thread, Event
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

            with self.start_monitoring(file):
                process = Popen([self.editor, file.name])
                try:
                    process.wait(Config.get().read('timeout') * 60 or None)
                except TimeoutExpired:
                    process.kill()
                    process.wait()
                    self.clear()
                    print("Editor timed out, killing and storing last saved content")

    @property
    def editor(self):
        if not hasattr(self, '_editor'):
            self._editor = os.environ.get('EDITOR')
            if not self._editor:
                print("EDITOR environment variable not set.")
                while not self._editor:
                    self._editor = input("Type your preferred editor: ")
        return self._editor

    @contextmanager
    def start_monitoring(self, file):
        stop_event = Event()
        monitor_thread = Thread(target=self.monitor, args=(file, stop_event))
        monitor_thread.start()

        try:
            yield
        finally:
            stop_event.set()
            monitor_thread.join()

    def monitor(self, file, stop_event):
        last_mtime = os.stat(file.name).st_mtime
        while not stop_event.is_set():
            stop_event.wait(0.5)
            new_mtime = os.stat(file.name).st_mtime
            if new_mtime == last_mtime:
                continue
            new_mtime = last_mtime
            new_content = file.read()
            file.seek(0)
            if new_content == self.content:
                continue
            self.content = new_content
            self.storage.set(self.encryption.encrypt(new_content))

    def clear(self):
        if os.name != 'nt':
            os.system('reset')
            os.system('clear')
        else:
            os.system('cls')
