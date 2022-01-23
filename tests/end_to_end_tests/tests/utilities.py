"""Various utilities used in the tests"""

import os
from pathlib import Path
import subprocess
from typing import Optional, Tuple

# pylint:disable=protected-access

FILES_AND_ESCAPED_CONTENTS = (
    ("one_line.txt", "abcdef"),
    ("two_lines.txt", "one line\\ntwo lines"),
    ("tabs.txt", "a\\tb\\tcde\\tfg"),
)

OUTPUT_TO_FILE_FLAGS = ("-o", "--output")

TEST_FILES_DIR = (
    Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) / "test_files"
)


def get_cpp11_embed_path() -> str:
    """:returns: the path to the executable"""
    if get_cpp11_embed_path._cpp11_embed_path is None:
        raise RuntimeError("Path not set up yet")
    return get_cpp11_embed_path._cpp11_embed_path


get_cpp11_embed_path._cpp11_embed_path = None


def get_expected_text_data_header(
    identifier_name: str, use_header_guard: bool, string_literal_contents: str
) -> str:
    """:returns: the contents of the header file"""
    if use_header_guard:
        header_guard = identifier_name.upper()
        return f'#ifndef {header_guard}\n#define {header_guard}\n\nconstexpr char {identifier_name}[] = "{string_literal_contents}";\n\n#endif\n'
    return f'#pragma once\n\nconstexpr char {identifier_name}[] = "{string_literal_contents}";\n'


def run_cpp11_embed_arbitrary_arguments(
    arguments: Tuple[str], standard_input: Optional[str] = None
) -> subprocess.CompletedProcess[str]:
    """Note: use run_cpp11_embed instead unless you are trying
    to pass invalid arguments.

    Runs cpp11_embed and captures the output
    :returns: the result from subprocess.run
    """
    # pylint:disable=subprocess-run-check
    cmd = (get_cpp11_embed_path(),) + arguments
    return subprocess.run(cmd, capture_output=True, text=True, input=standard_input)


def run_cpp11_embed(
    input_filename: str,
    identifier_name: str,
    use_header_guard: bool,
    other_arguments: Tuple[str] = tuple(),
    standard_input: Optional[str] = None,
) -> subprocess.CompletedProcess[str]:
    """Runs cpp11_embed and captures the output
    :returns: the result from subprocess.run
    """
    header_guard_flag = ("--use-header-guard",) if use_header_guard else tuple()
    arguments = (input_filename, identifier_name) + header_guard_flag + other_arguments
    return run_cpp11_embed_arbitrary_arguments(arguments, standard_input=standard_input)
