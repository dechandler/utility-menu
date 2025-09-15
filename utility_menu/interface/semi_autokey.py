"""
Puts preconfigured phrases into the clipboard

Inspired by autokey, but without key-monitoring

"""
import logging
import os
import time
from functools import cached_property
from subprocess import Popen, PIPE


from .cli import CliInterface

from ..menu import MenuInterface
from ..utility import ClipboardUtils


log = logging.getLogger("utility_menu")


class SemiAutokeyUtilityMenu(CliInterface):


    def __init__(self, config):

        self.config = config


    def handle_args(self, args):
        """
        Load configured phrases
        Query the user to select a phrase
        Copy the phrase contents into the clipboard
        Overwrite after past_ttl if configured to do so

        """
        # Query the user to select a phrase
        selection = MenuInterface(
            [*self.phrases],
            prompt="Phrases",
            config=self.config
        ).selection
        if not selection:
            log.debug("SemiAutokey: No menu selection")
            return
        log.info(f"SemiAutokey selection: {selection}")

        # Copy the phrase contents into the clipboard
        clipboard = ClipboardUtils()
        clipboard.copy_text(self.phrases[selection])

        # Overwrite after past_ttl if configured to do so
        if self.config['paste_ttl'] in [0, -1, None, {}, False]:
            return
        time.sleep(self.config['paste_ttl'])
        if clipboard.contents() == self.phrases[selection]:
            clipboard.copy_text('')


    @cached_property
    def phrases(self):
        """
        Dict of named phrases, loaded from files in phrases_dir

        """
        phrases = {}

        # Determine the search directory for phrases
        config_dir = os.path.dirname(self.config['config_path'])
        phrases_dir = (
            os.path.expanduser(self.config.get('phrases_dir', ''))
            or os.path.join(config_dir, "phrases")
        )
        if not os.path.isabs(phrases_dir):
            phrases_dir = os.path.join(config_dir, phrases_dir)
        log.info(f"Using phrases_dir {phrases_dir}")

        # Compile phrases by relpath to phrases_dir
        for root, dirs, files in os.walk(phrases_dir):
            for fname in files:
                path = os.path.join(root, fname)
                with open(path) as fh:
                    phrase = fh.read()
                relpath = os.path.relpath(path, phrases_dir)
                log.debug(f"Loaded phrase '{relpath}': '{phrase}'")
                phrases[relpath] = phrase

        return phrases
