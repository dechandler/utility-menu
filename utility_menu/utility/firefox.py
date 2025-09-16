
import logging
import os
import psutil
import signal

from configparser import ConfigParser
from functools import cached_property
from subprocess import Popen

log = logging.getLogger("utility_menu")


class FirefoxUtils:


    def __init__(self):

        self.firefox = "firefox"


    def start_profile(self, profile_name):

        cmd = [
            self.firefox,
            "-P", profile_name
        ]
        log.debug(f"Forking firefox process, profile {profile_name}")
        Popen(cmd, start_new_session=True)


    def kill_profile(self, profile_name):

        if profile_name not in self.running_profiles:
            log.warn(f"Profile {profile_name} not apparently running")
            return

        pid = self.running_profiles[profile_name]
        log.info(f"Killing firefox: PID {pid}, Profile {profile_name}")   
        os.kill(self.running_profiles[profile_name], signal.SIGKILL)


    @cached_property
    def configured_profiles(self):

        profiles = []

        profiles_ini = ConfigParser()
        profiles_ini.read(os.path.expanduser("~/.mozilla/firefox/profiles.ini"))

        for profile in profiles_ini.values():
            log.debug(f'Read in profile {profile}')
            profile = dict(profile)
            profiles.append(profile.get('name'))

        return profiles


    @cached_property
    def running_profiles(self):

        running_profiles = {}
        for proc in psutil.process_iter(['name', 'pid', 'cmdline']):
            if proc.name() != "firefox":
                continue
            try:
                arg_index = proc.info['cmdline'].index('-P')
            except ValueError:
                log.debug(f"Firefox instance with unspecified profile: {dict(proc.info)}")
                continue
            if len(proc.info['cmdline']) == arg_index + 1:
                continue

            log.debug(f"{arg_index}")
            log.debug(f"Profile command: { {' '.join(proc.info['cmdline'])} }")
            profile_name = proc.info['cmdline'][arg_index + 1]

            log.debug(f"Profile found running: {profile_name}")
            running_profiles[profile_name] = proc.info['pid']


        return running_profiles
