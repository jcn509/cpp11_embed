import subprocess
from typing import List
import os
from pathlib import Path

import pytest

from .cpp11_embed_path import get_cpp11_embed_path

_TEST_FILES_DIR = Path(os.path.dirname(__file__)) / "test_files"


def run_cpp11_embed(
    input_filename: str, identifier_name: str, other_arguments: List[str] = []
):
    cmd = [get_cpp11_embed_path(), input_filename, identifier_name] + other_arguments
    return subprocess.run(cmd, capture_output=True, text=True)


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize(
    "file_name, expected_string_literal_contents",
    (
        ("one_line.txt", "abcdef"),
        ("two_lines.txt", "one line\\ntwo lines"),
        ("tabs.txt", "a\\tb\\tcde\\tfg"),
    ),
)
def test_successful_file_read(
    identifier_name: str, file_name: str, expected_string_literal_contents: str
):
    result = run_cpp11_embed(_TEST_FILES_DIR / file_name, identifier_name)
    assert (
        result.stdout
        == f'#pragma once\n\nconstexpr char* {identifier_name} = "{expected_string_literal_contents}";\n'
    )
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"
