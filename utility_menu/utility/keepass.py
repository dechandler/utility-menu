"""
To add session persistence, this wrapper uses gpg to encrypt and save
the keepass vault password to a private, volatile file in /dev/shm

The keepass vault password is queried only once per boot or cleanup job,
and gpg-agent provides a good interface for unlock persistence and expiry

"""
import logging
import os
import pwd
import sys
import time
from functools import cached_property
from subprocess import Popen, PIPE

import pykeepass

from ..menu import MenuInterface

from .gpg import GpgUtils
from .clipboard import ClipboardUtils


log = logging.getLogger("utility_menu")


class KeepassUtils:

    def __init__(self, vault_name, gpg_id, keepass_db_path, max_attempts, keepass_key=None):

        self.vault_name = vault_name
        self.gpg_id = gpg_id
        self.keepass_db_path = keepass_db_path
        self.max_attempts = max_attempts

        self.keepass_key = keepass_key

        username = pwd.getpwuid(os.getuid())[0]
        self.key_path = f"/dev/shm/keepass-{username}/{vault_name}.gpg"

        self.gpg = GpgUtils()

        self._keepass = None


    @property
    def keepass(self):

        if self._keepass:
            return self._keepass

        try:
            keepass = pykeepass.PyKeePass(
                self.keepass_db_path, password=self.keepass_key
            )
        except pykeepass.exceptions.CredentialsError:
            log.warn("Incorrect password, deleting cached pass")
            os.remove(self.key_path)
            self.attempts = self.attempts + 1
            if self.attempts > self.config['max_attempts']:
                sys.exit(1)
            return self.keepass

        self._keepass = keepass
        return keepass


    def get_entry(self, entry_path):

        entry = self.keepass.find_entries(path=entry_path)
        entry_data = {
            'username': entry.username,
            'password': entry.password,
            'url': entry.url,
            #'title': entry.title,
            'notes': entry.notes,
            'otp': entry.otp
        }
        entry_data.update(entry.custom_properties)

        return { k: v for k, v in entry_data.items() if v }


    @property
    def entries(self):
        return self.keepass.entries



    def store_keepass_key(self, keepass_key):

        self.keepass_key = keepass_key

        gpg = GpgUtils()
        gpg.encrypt_to_file(self.key_path, keepass_key, self.gpg_id)

    def get_stored_key(self):

        if not os.path.isfile(self.key_path):
            return

        self.keepass_key = self.gpg.decrypt_file(self.key_path, self.gpg_id)
        return self.keepass_key
