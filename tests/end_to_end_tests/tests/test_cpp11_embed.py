"""Basic end to end tests"""

import os
from pathlib import Path

import pytest

from .utilities import run_cpp11_embed

_TEST_FILES_DIR = Path(os.path.dirname(__file__)) / "test_files"

_FILES_AND_ESCAPED_CONTENTS = (
    ("one_line.txt", "abcdef"),
    ("two_lines.txt", "one line\\ntwo lines"),
    ("tabs.txt", "a\\tb\\tcde\\tfg"),
)

_OUTPUT_TO_FILE_FLAGS = ("-o", "--output")


def _get_expected_header(identifier_name: str, string_literal_contents: str) -> str:
    return f'#pragma once\n\nconstexpr char* {identifier_name} = "{string_literal_contents}";\n'


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize(
    "file_name, expected_string_literal_contents", _FILES_AND_ESCAPED_CONTENTS
)
def test_successful_file_input_output_to_stdout(
    identifier_name: str, file_name: str, expected_string_literal_contents: str
):
    """Test that a file can be read successfully and the correct header is
    generated and printed to standard output.

    stderror
    """
    result = run_cpp11_embed(_TEST_FILES_DIR / file_name, identifier_name)
    assert result.stdout == _get_expected_header(
        identifier_name, expected_string_literal_contents
    )
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize(
    "file_name, expected_string_literal_contents", _FILES_AND_ESCAPED_CONTENTS
)
def test_successful_stdin_output_to_stdout(
    identifier_name: str, file_name: str, expected_string_literal_contents: str
):
    """Test that standard input can be read successfully and the correct header
    is generated and printed to standard output.

    stderror
    """
    file_contents = Path(_TEST_FILES_DIR / file_name).read_text()
    result = run_cpp11_embed("-", identifier_name, standard_input=file_contents)
    assert result.stdout == _get_expected_header(
        identifier_name, expected_string_literal_contents
    )
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize(
    "file_name, expected_string_literal_contents", _FILES_AND_ESCAPED_CONTENTS
)
@pytest.mark.parametrize("output_to_file_flag", _OUTPUT_TO_FILE_FLAGS)
@pytest.mark.parametrize("output_filename", ("out.txt", "other.h"))
def test_successful_file_input_output_to_file(
    identifier_name: str,
    file_name: str,
    expected_string_literal_contents: str,
    output_to_file_flag: str,
    output_filename: str,
    tmp_path: Path,
):
    """Test that a file can be read successfully and the correct header is
    generated and printed to standard output.

    stderror
    """
    output_file_path = tmp_path / output_filename
    result = run_cpp11_embed(
        _TEST_FILES_DIR / file_name,
        identifier_name,
        other_arguments=(output_to_file_flag, output_file_path),
    )
    assert result.stdout == "", "Nothing written to standard output"
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"

    assert output_file_path.read_text() == _get_expected_header(
        identifier_name, expected_string_literal_contents
    )


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize(
    "file_name, expected_string_literal_contents", _FILES_AND_ESCAPED_CONTENTS
)
@pytest.mark.parametrize("output_to_file_flag", _OUTPUT_TO_FILE_FLAGS)
@pytest.mark.parametrize("output_filename", ("out.txt", "other.h"))
def test_successful_stdin_output_to_file(
    identifier_name: str,
    file_name: str,
    expected_string_literal_contents: str,
    output_to_file_flag: str,
    output_filename: str,
    tmp_path: Path,
):
    """Test that standard input can be read successfully and the correct header
    is generated and printed to standard output.

    stderror
    """
    output_file_path = tmp_path / output_filename
    file_contents = Path(_TEST_FILES_DIR / file_name).read_text()
    result = run_cpp11_embed(
        "-",
        identifier_name,
        standard_input=file_contents,
        other_arguments=(output_to_file_flag, output_file_path),
    )
    assert result.stdout == ""
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"

    assert output_file_path.read_text() == _get_expected_header(
        identifier_name, expected_string_literal_contents
    )
