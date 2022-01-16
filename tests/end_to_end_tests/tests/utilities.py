"""Various utilities used in the tests"""

import subprocess
from typing import Tuple

# pylint:disable=protected-access


def get_cpp11_embed_path() -> str:
    """:returns: the path to the executable"""
    if get_cpp11_embed_path._cpp11_embed_path is None:
        raise RuntimeError("Path not set up yet")
    return get_cpp11_embed_path._cpp11_embed_path


get_cpp11_embed_path._cpp11_embed_path = None


def run_cpp11_embed(
    input_filename: str, identifier_name: str, other_arguments: Tuple[str] = tuple()
):
    """Runs cpp11_embed and captures the output
    :returns: the result from subprocess.run
    """
    # pylint:disable=subprocess-run-check
    cmd = (get_cpp11_embed_path(), input_filename, identifier_name) + other_arguments
    return subprocess.run(cmd, capture_output=True, text=True)
