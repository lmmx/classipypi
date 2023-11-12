from pathlib import Path

from ..interfaces import ListingConfig, SelectorConfig
from .ai_model import generate_tag_guided_model, initialise_model, run_inference
from .listing import list_tags
from .tag_data_models import model_tag_hierarchies
from .tag_trees import nest_tags

__all__ = ["select_tags"]


def describe_source(source: Path):
    raise NotImplementedError("Description generation for a given path not implemented")


def select_tags(config: SelectorConfig) -> list[str]:
    # Extract the listing config from the selection config (note: currently no overlap)
    list_config = ListingConfig.model_validate(config.model_dump())
    tags = list_tags(list_config)
    # Convert the list of tags into a nested dict structure of tag paths
    tag_hierarchy = nest_tags(tags, formatted=False)
    TagHierarchyModel = model_tag_hierarchies(tag_hierarchy)
    # Use 'query' or extract description from 'source' for tag generation
    desc = config.query if config.query else describe_source(config.source)
    llm = initialise_model(config)
    suggested_tags = []
    for tag_type in TagHierarchyModel.__fields__:
        tag_sublist = [t for t in tags if t.startswith(f"{tag_type} :: ")]
        guided_model = generate_tag_guided_model(model=llm, tags=tag_sublist)
        # Generate tags based on the description
        suggestion = run_inference(guided_model, descriptions=[desc])[0]
        suggested_tags.append(suggestion)
    return suggested_tags
