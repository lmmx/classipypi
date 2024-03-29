from collections import defaultdict

__all__ = ["build_nested_dict", "nest_tags"]


def build_nested_dict():
    """
    Helper function to create a nested defaultdict.
    """
    return defaultdict(build_nested_dict)


def defaultdict_to_dict(d):
    if isinstance(d, defaultdict):
        # Convert the defaultdict to a regular dict
        d = dict(d)
    for key, value in d.items():
        if isinstance(value, defaultdict):
            # Recursively process nested defaultdicts
            d[key] = defaultdict_to_dict(value)
    return d


def nest_tags(tags: list[str], formatted: bool = True) -> str | dict:
    """
    Organize tags into a nested dictionary structure.
    """
    nested_tags = build_nested_dict()
    for tag in tags:
        path = tag.split(" :: ")
        current_level = nested_tags
        for part in path:
            current_level = current_level[part]

    def format_nested_tags(nested_dict, level=0):
        """
        Function to format the nested tags as a string
        """
        result = ""
        for key, sub_dict in nested_dict.items():
            prefix = " " * 2 * level  # 2 spaces per indentation level
            result += f"{prefix}{key}\n"
            if isinstance(sub_dict, defaultdict):
                result += format_nested_tags(sub_dict, level + 1)
        return result

    if formatted:
        return format_nested_tags(nested_tags).rstrip("\n")
    else:
        return defaultdict_to_dict(nested_tags)
