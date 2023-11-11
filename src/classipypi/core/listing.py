import tomli_w
from trove_classifiers import sorted_classifiers

from ..interfaces import ListingConfig
from .tag_trees import nest_tags

__all__ = ["list_tags"]


def list_tags(config: ListingConfig) -> list[str]:
    tags = sorted_classifiers
    # Filtering
    if config.include:
        tags = [
            tag
            for tag in tags
            for query in config.include
            if (
                (query.lower() in tag.lower())
                if config.case_insensitive
                else (query in tag)
            )
        ]
    if config.exclude:
        tags = [
            tag
            for tag in tags
            for query in config.exclude
            if (
                (query.lower() not in tag.lower())
                if config.case_insensitive
                else (query not in tag)
            )
        ]
    # Presentation
    if config.group:
        tags = [nest_tags(tags)]
    elif config.toml:
        tags = [tomli_w.dumps({"classifiers": tags}).strip()]
    return tags
