
import json
import logging
import os

from functools import cached_property

import yaml

log = logging.getLogger("utility_menu")


class UtilityMenuConfig:

    @cached_property
    def config(self):

        """
        Set a default config, then load a config file

        The priority order is:
            Environment variable: DMENU_UTILS_CONFIG (~ accepted)
            $HOME/.config/dmenu-utils.yaml

        """

        # Set defaults
        config = {
            'menu_app': "wofi",
            'location': 3,
            'x_offset': 0,
            'line_max': 10,
            'log_dir': "~/.config/utility-menu/log",
            'log_level': "warning",
            'paste_ttl': 45,
            'utilities': {}
        }

        # Override defaults with options from first existing file
        search_paths = [
            os.environ.get("UTILITY_MENU_CONFIG", ""),
            "~/.config/utility-menu/config.yaml"
        ]
        for path_var in search_paths:
            path = os.path.expanduser(path_var)
            try:
                with open(path) as fh:
                    data = yaml.safe_load(fh)
                    config.update(data)
                    log.info(f"Config Path: {path}")
                break
            except FileNotFoundError:
                pass
            except yaml.scanner.ScannerError:
                log.error(f"File exists at {path} but is not YAML parseable, aborting...")
                sys.exit(1)
            except Exception as e:
                log.debug(f"unexpected exception while loading yaml ({e.__class__}): {e}")

        config['log_dir'] = os.path.expanduser(config['log_dir'])

        log.debug(f"Loaded config: {json.dumps(config)}")

        return config


    def get_utility(self, utility_name):

        config = {**self.config}

        utility = self.config['utilities'].get(utility_name, {})
        del config['utilities']

        config.update(utility)

        return config


    def items(self):

        return self.config.items()

    def __getitem__(self, key):

        return self.config.get(key)

    def __setitem__(self, key, value):

        self.config[key] = value
