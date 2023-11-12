from enum import Enum

from pydantic import create_model

__all__ = ["model_tag_hierarchies"]


class AutoNameEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


def model_tag_hierarchies(tag_hierarchy: dict):
    """
    Create a dynamic Pydantic model from the list of tags passed in, for use as a
    generation guide.
    """
    # top_level_keys = list(tag_hierarchy)
    top_enum_keys = [
        "Development Status",
        "Intended Audience",
        "Natural Language",  # It does not make sense to guess this tag
        "Typing",  # It does not make sense to guess this tag
    ]
    do_not_guess = {"Natural Language", "Typing"}
    # top_nested_keys = [k for k in top_level_keys if k not in top_enum_keys]  # TODO
    top_enums = {
        enum_key: AutoNameEnum(enum_key, [*tag_hierarchy[enum_key]])
        for enum_key in top_enum_keys
    }
    tag_hierarchy_model_fields = {
        field_name: (enum_type, ...)
        for field_name, enum_type in top_enums.items()
        if field_name not in do_not_guess
    }
    TagHierarchyModel = create_model("TagHierarchy", **tag_hierarchy_model_fields)
    return TagHierarchyModel
