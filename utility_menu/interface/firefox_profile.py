
import configparser
import logging
import os
import time

import pykeepass


from .cli import CliInterface

from ..menu import MenuInterface
from ..utility import FirefoxUtils



log = logging.getLogger("utility_menu")


class FirefoxProfileUtilityMenu(CliInterface):


    def __init__(self, config):

        self.config = config
        self.firefox = FirefoxUtils()

    def handle_args(self, _):

        configured_profiles = self.firefox.configured_profiles
        running_profiles = self.firefox.running_profiles

        menu = {}
        for profile_name in configured_profiles:
            if profile_name in running_profiles:
                option = f"Kill profile {profile_name} (PID {running_profiles[profile_name]})"
                running = True
            else:
                option = f"Start profile {profile_name}"
                running = False
            menu[option] = {
                'name': profile_name,
                'running': running
            }

        selection = menu[MenuInterface(
            [*menu],
            prompt="Firefox Profile Actions",
            config=self.config
        ).selection]

        if selection['running']:
            self.firefox.kill_profile(selection['name'])
        else:
            self.firefox.start_profile(selection['name'])
