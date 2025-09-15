"""


"""
import json
import logging
import os
import sys

from ..config import UtilityMenuConfig
from .cli import CliInterface
from .keepass import KeepassUtilityMenu


log = logging.getLogger("utility_menu")


class MainCli(CliInterface):

    def __init__(self):

        self.config = UtilityMenuConfig()

        self.configure_loggers(self.config['log_dir'], self.config['log_level'])
        log.debug(f"Starting Utility Menu; PID {os.getpid()}; args: {sys.argv[1:]}")
        log.debug(f"Run config: {json.dumps(dict(self.config.items()))}")

        self.operations = {
            'keepass': {
                'aliases': ['kp'],
                'handler': self.run_keepass_menu
            }
            # 'network_manager': {
            #     'aliases': ['nm', 'network-manager'],
            #     'handler': lambda: NetworkManagerUtilityMenu(self.config).handle_args
            # }

        }


    def run_keepass_menu(self, args):

        config = self.config.get_utility("keepass")

        KeepassUtilityMenu(config).handle_args(args)



    def configure_loggers(self, log_dir, log_level):

        os.makedirs(log_dir, exist_ok=True)

        datefmt = "%Y-%m-%d_%H:%M:%S"
        log.setLevel(getattr(logging, log_level.upper()))

        handler = logging.FileHandler(os.path.join(log_dir, "utility-menu.log"))
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)-7s %(message)s', datefmt=datefmt
        ))
        log.addHandler(handler)

        # handler = logging.StreamHandler()
        # log.addHandler(handler)
