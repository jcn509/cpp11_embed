"""Basic end to end tests"""

import os
from pathlib import Path

import pytest

from .utilities import run_cpp11_embed

_TEST_FILES_DIR = (
    Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) / "test_files"
)

_FILES_AND_ESCAPED_CONTENTS = (
    ("one_line.txt", "abcdef"),
    ("two_lines.txt", "one line\\ntwo lines"),
    ("tabs.txt", "a\\tb\\tcde\\tfg"),
)

_OUTPUT_TO_FILE_FLAGS = ("-o", "--output")


def _get_expected_text_data_header(
    identifier_name: str, use_header_guard: bool, string_literal_contents: str
) -> str:
    if use_header_guard:
        header_guard = identifier_name.upper()
        return f'#ifndef {header_guard}\n#define {header_guard}\n\nconstexpr char {identifier_name}[] = "{string_literal_contents}";\n\n#endif\n'
    return f'#pragma once\n\nconstexpr char {identifier_name}[] = "{string_literal_contents}";\n'


def _get_expected_binary_data_header(
    identifier_name: str, use_header_guard: bool, expected_data: str, expected_size: int
) -> str:
    if use_header_guard:
        header_guard = identifier_name.upper()
        return f"#ifndef {header_guard}\n#define {header_guard}\n\n#include <array>\n#include <cstdint>\n\nconstexpr std::array<uint8_t, {expected_size}> {identifier_name}{expected_data};\n\n#endif\n"
    return f"#pragma once\n\n#include <array>\n#include <cstdint>\n\nconstexpr std::array<uint8_t, {expected_size}> {identifier_name}{expected_data};\n"


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize("use_header_guard", (True, False))
@pytest.mark.parametrize(
    "file_name, expected_string_literal_contents", _FILES_AND_ESCAPED_CONTENTS
)
def test_successful_text_file_input_output_to_stdout(
    identifier_name: str,
    use_header_guard: bool,
    file_name: str,
    expected_string_literal_contents: str,
):
    """Test that a text file can be read successfully and the correct header
    is generated and printed to standard output.

    Also makes sure that the return code is 0 and nothing is written to
    standard error.
    """
    result = run_cpp11_embed(
        _TEST_FILES_DIR / file_name, identifier_name, use_header_guard
    )
    assert result.stdout == _get_expected_text_data_header(
        identifier_name, use_header_guard, expected_string_literal_contents
    )
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize("use_header_guard", (True, False))
@pytest.mark.parametrize(
    "file_name, expected_string_literal_contents", _FILES_AND_ESCAPED_CONTENTS
)
@pytest.mark.parametrize("help_flag", ("--help", "-h"))
def test_help_flag(
    identifier_name: str,
    use_header_guard: bool,
    file_name: str,
    expected_string_literal_contents: str,
    help_flag: str,
):
    """Ensure that when the help flag is used some help text is printed and
    the app exits with code 0 without doing any work.

    Also makes sure that nothing is written to standard error.
    """
    result = run_cpp11_embed(
        _TEST_FILES_DIR / file_name,
        identifier_name,
        use_header_guard,
        other_arguments=(help_flag,),
    )
    expected_header = _get_expected_text_data_header(
        identifier_name, use_header_guard, expected_string_literal_contents
    )
    assert (
        "Display this help menu" in result.stdout
    ), "Help menu appears to have been displayed"
    assert expected_header not in result.stdout, "No header produced"
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize("use_header_guard", (True, False))
@pytest.mark.parametrize(
    "file_name, expected_string_literal_contents", _FILES_AND_ESCAPED_CONTENTS
)
def test_successful_text_stdin_output_to_stdout(
    identifier_name: str,
    use_header_guard: bool,
    file_name: str,
    expected_string_literal_contents: str,
):
    """Test that textual data from standard input can be read successfully and
    the correct header is generated and printed to standard output.

    Also makes sure that the return code is 0 and nothing is written to
    standard error.
    """
    file_contents = Path(_TEST_FILES_DIR / file_name).read_text()
    result = run_cpp11_embed(
        "-", identifier_name, use_header_guard, standard_input=file_contents
    )
    assert result.stdout == _get_expected_text_data_header(
        identifier_name, use_header_guard, expected_string_literal_contents
    )
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize("use_header_guard", (True, False))
@pytest.mark.parametrize(
    "file_name, expected_string_literal_contents", _FILES_AND_ESCAPED_CONTENTS
)
@pytest.mark.parametrize("output_to_file_flag", _OUTPUT_TO_FILE_FLAGS)
@pytest.mark.parametrize("output_filename", ("out.txt", "other.h"))
def test_successful_text_file_input_output_to_file(
    identifier_name: str,
    use_header_guard: bool,
    file_name: str,
    expected_string_literal_contents: str,
    output_to_file_flag: str,
    output_filename: str,
    tmp_path: Path,
):
    """Test that a text file can be read successfully and the correct header
    is generated and written to a file.

    Also makes sure that the return code is 0 and nothing is written to
    standard error.
    """
    output_file_path = tmp_path / output_filename
    result = run_cpp11_embed(
        _TEST_FILES_DIR / file_name,
        identifier_name,
        use_header_guard,
        other_arguments=(output_to_file_flag, output_file_path),
    )
    assert result.stdout == "", "Nothing written to standard output"
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"

    assert output_file_path.read_text() == _get_expected_text_data_header(
        identifier_name, use_header_guard, expected_string_literal_contents
    )


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize("use_header_guard", (True, False))
@pytest.mark.parametrize(
    "file_name, expected_string_literal_contents", _FILES_AND_ESCAPED_CONTENTS
)
@pytest.mark.parametrize("output_to_file_flag", _OUTPUT_TO_FILE_FLAGS)
@pytest.mark.parametrize("output_filename", ("out.txt", "other.h"))
def test_successful_text_stdin_output_to_file(
    identifier_name: str,
    use_header_guard: bool,
    file_name: str,
    expected_string_literal_contents: str,
    output_to_file_flag: str,
    output_filename: str,
    tmp_path: Path,
):
    """Test that textual data from standard input can be read successfully and
    the correct header is generated and written to a file.

    Also makes sure that the return code is 0 and nothing is written to
    standard error.
    """
    output_file_path = tmp_path / output_filename
    file_contents = Path(_TEST_FILES_DIR / file_name).read_text()
    result = run_cpp11_embed(
        "-",
        identifier_name,
        use_header_guard,
        standard_input=file_contents,
        other_arguments=(output_to_file_flag, output_file_path),
    )
    assert result.stdout == ""
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"

    assert output_file_path.read_text() == _get_expected_text_data_header(
        identifier_name, use_header_guard, expected_string_literal_contents
    )


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize("use_header_guard", (True, False))
@pytest.mark.parametrize("binary_mode_flag", ("--binary-mode", "-b"))
def test_successful_binary_file_input_output_to_stdout(
    identifier_name: str, use_header_guard: bool, binary_mode_flag: str
):
    """Test that a binary file can be read successfully and the correct header
    is generated and written to a file.

    Also makes sure that the return code is 0 and nothing is written to
    standard error.
    """
    result = run_cpp11_embed(
        _TEST_FILES_DIR / "one_line.txt",
        identifier_name,
        use_header_guard,
        other_arguments=(binary_mode_flag,),
    )
    expected_data = "{97, 98, 99, 100, 101, 102}"
    assert result.stdout == _get_expected_binary_data_header(
        identifier_name, use_header_guard, expected_data, 6
    )
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize("use_header_guard", (True, False))
@pytest.mark.parametrize("binary_mode_flag", ("--binary-mode", "-b"))
def test_successful_binary_stdin_output_to_stdout(
    identifier_name: str, use_header_guard: bool, binary_mode_flag: str
):
    """Test that binary data can be read successfully from standard input and
    the correct header is generated and written to a file.

    Also makes sure that the return code is 0 and nothing is written to
    standard error.
    """
    file_contents = Path(_TEST_FILES_DIR / "one_line.txt").read_text()
    result = run_cpp11_embed(
        "-",
        identifier_name,
        use_header_guard,
        other_arguments=(binary_mode_flag,),
        standard_input=file_contents,
    )
    expected_data = "{97, 98, 99, 100, 101, 102}"
    assert _get_expected_binary_data_header(
        identifier_name, use_header_guard, expected_data, 6
    )
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"
