import defopt

from .config import ListingConfig, SelectorConfig
from .listing import list_tags
from .select import select_tags

__all__ = ["run_cli"]


def run_cli():
    commands = {"sel": SelectorConfig, "ls": ListingConfig}
    config = defopt.run(commands, no_negated_flags=True)
    print(f"Got {config=}")
    match config:
        case SelectorConfig():
            select_tags(config)
        case ListingConfig():
            list_tags(config)
