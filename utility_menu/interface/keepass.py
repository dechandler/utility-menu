
import logging
import os
import time
from subprocess import Popen, PIPE

import pykeepass


from .cli import CliInterface

from ..menu import MenuInterface
from ..utility import KeepassUtils, ClipboardUtils



log = logging.getLogger("utility_menu")


class KeepassUtilityMenu(CliInterface):


    def __init__(self, config):

        self.config = config

        self.attempts = 0


    def handle_args(self, args):

        self.vault_name = args.pop(0)
        config = self.get_vault_config(self.vault_name)

        self.keepass = KeepassUtils(
            self.vault_name,
            config['gpg_id'],
            config['db'],
            config['max_attempts']
        )

        # Get or set the stored keepass password
        keepass_key = self.keepass.get_stored_key()
        if not keepass_key:
            keepass_key = MenuInterface(
                [],
                prompt="Keepass Password",
                password_mode=True,
                config=config
            ).selection
            self.keepass.store_keepass_key(keepass_key)


        # Query for a keepass entry name
        menu_item_paths = self.get_entry_menu()

        selected_entry = MenuInterface(
            [*menu_item_paths],
            config=config,
            prompt="Accounts"
        ).selection

        # Retrieve entry attributes
        entry_data = self.keepass.get_entry(
            menu_item_paths[selected_entry].path
        )

        # Query for which attribute to return
        attribute = MenuInterface(
            [*entry_data],
            config=config,
            prompt="Attribute"
        ).selection
        secret = entry_data[attribute]

        # Copy secret into clipboard, then overwrite after a timeout
        clipboard = ClipboardUtils()
        clipboard.copy_text(secret)

        time.sleep(config['paste_ttl'])
        if clipboard.contents() == secret:
            clipboard.copy_text('')


    def get_entry_menu(self):

        # Construct menu items to select account entry
        menu_item_paths = {}
        name_collisions = [None]
        for entry in self.keepass.entries:
            name = entry.path[-1]
            long_name = f"{name} ({'/'.join(entry.path[:-1])})"

            # If collision second instance,
            # change first instance to indexed by long name
            # and mark as collision item
            if name in menu_item_paths:
                old_path = '/'.join(menu_item_paths[name].path[:-1])
                prev_long_name = f"{name} ({old_path})"
                menu_item_paths[prev_long_name] = menu_item_paths[name]
                del menu_item_paths[name]
                name_collisions.append(name)

            # Use long name if collisions are known
            if name in name_collisions:
                name = long_name

            menu_item_paths[name] = entry

        return menu_item_paths


    def get_vault_config(self, vault_name):

        config = {
            'max_attempts': 3
        }
        config.update({**self.config})
        del config['vaults']

        for vault in self.config['vaults']:
            if vault.get('name') == vault_name:
                config.update(vault)
                break

        # Expand ~ and relpaths to set db path
        db_base_dir = config.get('db_base_dir') or "~/.config/keepass"
        config['db'] = os.path.expanduser(
            config.get('db')
            or os.path.join(db_base_dir, vault_name, f"{vault_name}.kdbx")
        )
        if not os.path.isabs(config['db']):
            config['db'] = os.path.join(db_base_dir, config['db'])

        return config
