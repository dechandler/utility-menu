
import sys

from .interface import MainCli
from .exceptions import (
    NoMenuSelectionError,
    InvalidMenuSelectionError
)

def main():

    try:
        MainCli().handle_args(sys.argv[1:])
    except KeyboardInterrupt:
        pass
    except NoMenuSelectionError as e:
        print(f"NoMenuSelectionError: {e}")
    except InvalidMenuSelectionError as e:
        print(f"InvalidMenuSelectionError: {e}")
