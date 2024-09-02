"""Macros added to jinja namespaces by the mkdocs-macros plugin."""

from __future__ import annotations

from pathlib import Path as _Path


def define_env(env):
    """Define new function macros for the jinja namespace."""

    @env.macro
    def Path(path: str) -> _Path:
        """Make `pathlib.Path` available in inline template macros."""
        return _Path(path)
