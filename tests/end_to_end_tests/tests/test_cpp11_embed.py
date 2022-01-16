"""Basic end to end tests"""

import os
from pathlib import Path

import pytest

from .utilities import run_cpp11_embed

_TEST_FILES_DIR = Path(os.path.dirname(__file__)) / "test_files"


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize(
    "file_name, expected_string_literal_contents",
    (
        ("one_line.txt", "abcdef"),
        ("two_lines.txt", "one line\\ntwo lines"),
        ("tabs.txt", "a\\tb\\tcde\\tfg"),
    ),
)
def test_successful_file_read_stdout(
    identifier_name: str, file_name: str, expected_string_literal_contents: str
):
    """Test that a file can be read successfully and the correct header is
    generated and printed to stdout.

    stderror
    """
    result = run_cpp11_embed(_TEST_FILES_DIR / file_name, identifier_name)
    assert (
        result.stdout == f"#pragma once\n\nconstexpr char* {identifier_name} = "
        f'"{expected_string_literal_contents}";\n'
    )
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"
