from pytest import mark

from classipypi import list_tags
from classipypi.interfaces import ListingConfig


@mark.parametrize(
    "exclude,expected",
    [
        (
            [],
            [
                "Development Status :: 1 - Planning",
                "Development Status :: 2 - Pre-Alpha",
                "Development Status :: 3 - Alpha",
                "Development Status :: 4 - Beta",
                "Development Status :: 5 - Production/Stable",
                "Development Status :: 6 - Mature",
                "Development Status :: 7 - Inactive",
            ],
        ),
        (
            ["Alpha"],
            [
                "Development Status :: 1 - Planning",
                "Development Status :: 4 - Beta",
                "Development Status :: 5 - Production/Stable",
                "Development Status :: 6 - Mature",
                "Development Status :: 7 - Inactive",
            ],
        ),
    ],
)
def test_list_dev_statuses(exclude, expected):
    config = ListingConfig(include=["Development Status"], exclude=exclude)
    tags = list_tags(config)
    assert tags == expected


@mark.parametrize(
    "case_insensitive,search_query,expected",
    [
        (
            False,
            "search",
            [
                "Intended Audience :: Science/Research",
            ],
        ),
        (
            True,
            "search",
            [
                "Intended Audience :: Science/Research",
                "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
            ],
        ),
        (False, "SeArCh", []),
        (
            True,
            "SeArCh",
            [
                "Intended Audience :: Science/Research",
                "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
            ],
        ),
    ],
)
def test_list_tags_case_insensitivity_standard(
    case_insensitive,
    search_query,
    expected,
):
    config = ListingConfig(include=[search_query], case_insensitive=case_insensitive)
    tags = list_tags(config)
    assert tags == expected


toml_example_single = """classifiers = [
    "Intended Audience :: Science/Research",
]"""

toml_example_double = """classifiers = [
    "Intended Audience :: Science/Research",
    "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
]"""


@mark.parametrize(
    "case_insensitive,search_query,expected",
    [
        (False, "search", [toml_example_single]),
        (True, "search", [toml_example_double]),
    ],
)
def test_list_tags_case_insensitivity_toml(case_insensitive, search_query, expected):
    config = ListingConfig(
        include=[search_query],
        case_insensitive=case_insensitive,
        toml=True,
    )
    tags = list_tags(config)
    assert tags == expected


grouped_example_single = """Topic
  Text Processing
    Markup
      HTML"""

grouped_example_multi = """Topic
  Text Processing
    Markup
      HTML
      LaTeX
      Markdown
      SGML
      VRML
      XML
      reStructuredText"""


@mark.parametrize(
    "case_insensitive,search_query,expected",
    [
        (False, "Markup :: H", [grouped_example_single]),
        (True, "Markup", [grouped_example_multi]),
    ],
)
def test_list_tags_output(case_insensitive, search_query, expected):
    config = ListingConfig(include=[search_query], group=True)
    tags = list_tags(config)
    assert tags == expected
