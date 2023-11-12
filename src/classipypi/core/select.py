from pathlib import Path

from ..interfaces import ListingConfig, SelectorConfig
from .ai_model import generate_tag_guided_model, initialise_model, run_inference
from .listing import list_tags

__all__ = ["select_tags"]


def describe_source(source: Path):
    raise NotImplementedError("Description generation for a given path not implemented")


def select_tags(config: SelectorConfig) -> list[str]:
    model = initialise_model(config)
    # Extract the listing config from the selection config (note: currently no overlap)
    list_config = ListingConfig.model_validate(config.model_dump())
    all_tags = list_tags(list_config)
    tag_guided_model = generate_tag_guided_model(model=model, tags=all_tags)
    # Use 'query' or extract description from 'source' for tag generation
    desc = config.query if config.query else describe_source(config.source)
    # Generate tags based on the description
    suggested_tags = run_inference(tag_guided_model, descriptions=[desc], tags=all_tags)
    return suggested_tags
