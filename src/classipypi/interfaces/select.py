from pathlib import Path

from pydantic import BaseModel, model_validator

from .display import DisplayConfig

__all__ = ["SourceConfig", "SelectorConfig"]


class SourceConfig(BaseModel):
    query: str | None = None
    source: Path | None = None

    @model_validator(mode="after")
    @classmethod
    def mutually_exclusive_and_required(cls, self):
        if self.query and self.source:
            raise ValueError("Cannot provide both 'query' and 'source'.")
        if not (self.query or self.source):
            raise ValueError("Must provide one of 'query' and 'source'.")
        return self


class AIConfig(BaseModel):
    nn_model: str = "HuggingFaceH4/zephyr-7b-beta"
    use_cpu: bool = False
    use_4bit: bool = True


class SelectorConfig(AIConfig, DisplayConfig, SourceConfig):
    """
    Configure input source and output display.

      :param query: The query string.
      :param source: The source code.
      :param nn_model: Name of a HuggingFace Transformers model to use for inference.
      :param use_cpu: Whether to run inference on the CPU.
      :param use_4bit: Whether to run quantised 4-bit models (bitsandbytes).
      :param toml: Whether to display the tags as a TOML-compatible list.
      :param group: Whether to display tags grouped by section.
    """
