
from .wofi import WofiMenu


class MenuInterface:

    def __new__(cls,
            entries,
            config=None,
            menu_app=None,
            prompt="",
            password_mode=False,
            location=None,
            x_offset=None,
            line_max=None,
            extra_args=None

        ):

        config = config or {}

        _extra_args = [ *config.get('extra_args', []) ]
        _extra_args.extend(extra_args or [])

        menu_app = menu_app or config.get('menu_app') or "wofi"

        Menu = {
            #'dmenu': Dmenu,
            #'rofi': RofiMenu,
            'wofi': WofiMenu
        }[menu_app]

        return Menu(
            entries,
            prompt,
            password_mode,
            location or config.get('location') or 1,
            x_offset or config.get('x_offset') or 0,
            line_max or config.get('line_max') or 10,
            _extra_args
        )
