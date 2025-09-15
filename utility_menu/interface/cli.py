
import logging

from ..menu import MenuInterface

log = logging.getLogger('utility-menu')

class CliInterface:

    help_message = "TODO: Make Help"
    default_operation = 'help'
    operations = {}


    def menu(self, config, entries, prompt=None, password_mode=False, extra_args=None):

        _extra_args = [ *config['extra_args'] ]
        _extra_args.extend(extra_args)

        menu = MenuInterface(
            entries,
            **{
                'menu_app': config['menu_app'],
                'prompt': prompt,
                'password_mode': password_mode,
                'location': config['location'],
                'x_offset': config['x_offset'],
                'line_max': config['line_max'],
                'extra_args': _extra_args
            }
        )



    def handle_args(self, args, default_operation='help'):

        self.operations['help'] = (
            self.operations.get('help')
            or {'handler': self.print_help}
        )

        subcommands = {}
        for name, op in self.operations.items():
            for op_name in op.get('aliases', []) + [name]:
                subcommands[op_name] = {
                    'name': name,
                    'handler': op['handler']
                }

        if not args or args[0] not in subcommands.keys():
            args = [self.default_operation] + args

        self.op_name = args.pop(0)
        log.debug(f"Subcommand {self.op_name} with args: {args}")

        handler = subcommands[self.op_name]['handler']
        if handler.__name__ == "<lambda>":
            handler = handler()
        handler(args)


    def print_help(self, args):

        print(self.help_message)
