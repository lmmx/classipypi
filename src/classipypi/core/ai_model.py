import logging
from textwrap import dedent

import outlines.models as models
import outlines.text.generate as generate
import torch

from ..interfaces import SelectorConfig

__all__ = ["initialise_model", "generate_tag_guided_model"]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def initialise_model(config: SelectorConfig):
    """
    Initialises and returns the AI model based on the provided model name.
    """
    if config.use_cpu:
        model = models.transformers(config.nn_model, device=None)
    else:
        # device = "cuda" if torch.cuda.is_available() else "cpu"
        # https://github.com/tloen/alpaca-lora/issues/21#issuecomment-1473318920
        kw = dict(load_in_4bit=config.use_4bit)
        if config.use_4bit:
            kw["torch_dtype"] = torch.float32
        model = models.transformers(config.nn_model, device={"": 0}, model_kwargs=kw)
    return model


def generate_tag_guided_model(model, tags):
    """
    Creates and returns a tag guided model generator.
    """
    return generate.choice(model, tags)


def run_inference(tag_guided_model_generator, descriptions, candidate_tags):
    """
    Runs a series of inferences using the provided generator and descriptions.
    """
    feature = (
        dedent(
            """
    various features (development status, environment, framework, intended
    audience, license, natural language, operating system, programming language, topic,
    and type hinting)
    """,
        )
        .strip()
        .replace("\n", " ")
    )
    tag_list = "\n    ".join(candidate_tags)
    system, user, assistant = "<|system|>", "<|user|>", "<|assistant|>"
    # feature = "intended audience"
    # demo1, expect1 = (
    #     "a program to train supermarket staff in how to interact with customers",
    #     "Customer Service",
    # )
    # demo2, expect2 = ("a floor plan generator for factory designers", "Manufacturing")
    # icl = """
    # For example, if a project is described as {demo1} then its {feature} is {expect1}.

    # If a project is described as {demo2} then its {feature} is {expect2}.
    # """
    prompt = dedent(
        f"""
    {system}
    You are a Python software project labelling assistant.

    You have the following labels to describe the {feature} of the package:

    {tag_list}

    {user}
    What label should be given to a project with the following description?

    """,
    ).lstrip()
    logger.debug(f"PROMPT: {prompt}")
    suggested_tags = [
        tag_guided_model_generator(f"{prompt}{desc}\n\n{assistant}\n")
        for desc in descriptions
    ]
    return suggested_tags
