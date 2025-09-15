"""

"""
import logging

from subprocess import Popen, PIPE

import yaml

from ..exceptions import NoMenuSelectionError


log = logging.getLogger("utility_menu")


class WofiMenu:

    def __init__(self,
            entries,
            prompt,
            password_mode,
            location,
            x_offset,
            line_max,
            extra_args
        ):
        """
        :param dmenu_app: currently can be "wofi" or "rofi"
        :type dmenu_app: str
        :param config: currently uses 'location', 'line_max', and 'x_offset'(wofi only)
        :type config: dict

        """
        self.entries = entries
        self.prompt = prompt
        self.password_mode = password_mode

        self.location = location
        self.x_offset = x_offset
        self.line_max = line_max

        self.extra_args = extra_args


    @property
    def selection(self):
        """
        Constructs a command for dmenu-compatable selectors, runs it,
        then returns the result

        """
        b_entries = [e.encode('utf-8') for e in self.entries]
        log.debug(b_entries)
        cmd = [
            "wofi", "--dmenu", "-i",
            "--location", str(self.location),
            "--xoffset", str(self.x_offset),
        ]
        if self.prompt:
            cmd.extend(["--prompt", self.prompt])
        if self.password_mode:
            cmd.append("--password")

        lines = len(self.entries) + 3 if self.entries else 1
        lines = self.line_max if lines > self.line_max else lines
        cmd.extend(["--lines", str(lines)])

        cmd.extend(self.extra_args)

        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        p.stdin.write(b'\n'.join(b_entries))
        out, err = p.communicate()

        if not out:
            raise NoMenuSelectionError(f"No selection for '{self.prompt}'")

        return out.decode('utf-8').strip()
