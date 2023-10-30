from sys import stderr
from textwrap import indent

import defopt
from pydantic import ValidationError

from .config import ListingConfig, SelectorConfig
from .listing import list_tags
from .select import select_tags

__all__ = ["run_cli"]


def run_cli():
    commands = {"sel": SelectorConfig, "ls": ListingConfig}
    try:
        config = defopt.run(commands, no_negated_flags=True)
    except ValidationError as ve:
        error_msgs = "\n".join(str(e["ctx"]["error"]) for e in ve.errors())
        print("The command you ran was invalid for the following reason:", file=stderr)
        print(indent(error_msgs, prefix="- "), end="\n\n", file=stderr)
        chosen_command = {v.__name__: k for k, v in commands.items()}[ve.title]
        try:
            defopt.run(commands[chosen_command], argv=["-h"])
        except SystemExit as exc:
            exc.code = 1
            raise
    else:
        print(f"Got {config=}")
        match config:
            case SelectorConfig():
                select_tags(config)
            case ListingConfig():
                list_tags(config)
