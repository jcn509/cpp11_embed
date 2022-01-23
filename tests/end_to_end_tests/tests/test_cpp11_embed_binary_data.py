"""Tests to ensure that a valid header file can be generated from binary data"""

from pathlib import Path

import pytest

from .utilities import OUTPUT_TO_FILE_FLAGS, run_cpp11_embed, TEST_FILES_DIR


def _get_expected_binary_data_header(
    identifier_name: str, use_header_guard: bool, expected_data: str, expected_size: int
) -> str:
    if use_header_guard:
        header_guard = identifier_name.upper()
        return f"#ifndef {header_guard}\n#define {header_guard}\n\n#include <array>\n#include <cstdint>\n\nconstexpr std::array<uint8_t, {expected_size}> {identifier_name}{expected_data};\n\n#endif\n"
    return f"#pragma once\n\n#include <array>\n#include <cstdint>\n\nconstexpr std::array<uint8_t, {expected_size}> {identifier_name}{expected_data};\n"


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize("use_header_guard", (True, False))
@pytest.mark.parametrize("binary_mode_flag", ("--binary-mode", "-b"))
def test_successful_binary_file_input_output_to_stdout(
    identifier_name: str, use_header_guard: bool, binary_mode_flag: str
):
    """Test that a binary file can be read successfully and the correct header
    is generated and printed to standard output.

    Also makes sure that the return code is 0 and nothing is written to
    standard error.
    """
    result = run_cpp11_embed(
        TEST_FILES_DIR / "one_line.txt",
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
@pytest.mark.parametrize("output_to_file_flag", OUTPUT_TO_FILE_FLAGS)
@pytest.mark.parametrize("output_filename", ("out.txt", "other.h"))
def test_successful_binary_file_input_output_to_file(
    identifier_name: str,
    use_header_guard: bool,
    binary_mode_flag: str,
    output_to_file_flag: str,
    output_filename: str,
    tmp_path: Path,
):
    """Test that a binary file can be read successfully and the correct header
    is generated and written to a file.

    Also makes sure that the return code is 0 and nothing is written to
    standard output or standard error.
    """
    output_file_path = tmp_path / output_filename
    result = run_cpp11_embed(
        TEST_FILES_DIR / "one_line.txt",
        identifier_name,
        use_header_guard,
        other_arguments=(binary_mode_flag, output_to_file_flag, output_file_path),
    )
    expected_data = "{97, 98, 99, 100, 101, 102}"
    assert result.stdout == "", "Nothing written to standard output"
    assert output_file_path.read_text() == _get_expected_binary_data_header(
        identifier_name, use_header_guard, expected_data, 6
    ), "Correct header written to file"
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize("use_header_guard", (True, False))
@pytest.mark.parametrize("binary_mode_flag", ("--binary-mode", "-b"))
def test_successful_binary_stdin_output_to_stdout(
    identifier_name: str, use_header_guard: bool, binary_mode_flag: str
):
    """Test that binary data can be read successfully from standard input and
    the correct header is generated and printed to standard output.

    Also makes sure that the return code is 0 and nothing is written to
    standard error.
    """
    file_contents = Path(TEST_FILES_DIR / "one_line.txt").read_text()
    result = run_cpp11_embed(
        "-",
        identifier_name,
        use_header_guard,
        other_arguments=(binary_mode_flag,),
        standard_input=file_contents,
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
@pytest.mark.parametrize("output_to_file_flag", OUTPUT_TO_FILE_FLAGS)
@pytest.mark.parametrize("output_filename", ("out.txt", "other.h"))
def test_successful_binary_stdin_output_to_file(
    identifier_name: str,
    use_header_guard: bool,
    binary_mode_flag: str,
    output_to_file_flag: str,
    output_filename: str,
    tmp_path: Path,
):
    """Test that binary data can be read successfully from standard input and
    the correct header is generated and written to a file.

    Also makes sure that the return code is 0 and nothing is written to
    standard output or standard error.
    """
    file_contents = Path(TEST_FILES_DIR / "one_line.txt").read_text()
    output_file_path = tmp_path / output_filename
    result = run_cpp11_embed(
        "-",
        identifier_name,
        use_header_guard,
        other_arguments=(binary_mode_flag, output_to_file_flag, output_file_path),
        standard_input=file_contents,
    )
    expected_data = "{97, 98, 99, 100, 101, 102}"
    assert result.stdout == "", "Nothing written to standard output"
    assert output_file_path.read_text() == _get_expected_binary_data_header(
        identifier_name, use_header_guard, expected_data, 6
    ), "Correct header written to file"
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"
