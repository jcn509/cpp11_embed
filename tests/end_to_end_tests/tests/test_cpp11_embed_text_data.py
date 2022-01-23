"""Tests to ensure that a valid header file can be generated from textual data"""

from pathlib import Path

import pytest

from .utilities import (
    FILES_AND_ESCAPED_CONTENTS,
    get_expected_text_data_header,
    OUTPUT_TO_FILE_FLAGS,
    run_cpp11_embed,
    TEST_FILES_DIR,
)


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize("use_header_guard", (True, False))
@pytest.mark.parametrize(
    "file_name, expected_string_literal_contents", FILES_AND_ESCAPED_CONTENTS
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
        TEST_FILES_DIR / file_name, identifier_name, use_header_guard
    )
    assert result.stdout == get_expected_text_data_header(
        identifier_name, use_header_guard, expected_string_literal_contents
    )
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize("use_header_guard", (True, False))
@pytest.mark.parametrize(
    "file_name, expected_string_literal_contents", FILES_AND_ESCAPED_CONTENTS
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
    file_contents = Path(TEST_FILES_DIR / file_name).read_text()
    result = run_cpp11_embed(
        "-", identifier_name, use_header_guard, standard_input=file_contents
    )
    assert result.stdout == get_expected_text_data_header(
        identifier_name, use_header_guard, expected_string_literal_contents
    )
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize("use_header_guard", (True, False))
@pytest.mark.parametrize(
    "file_name, expected_string_literal_contents", FILES_AND_ESCAPED_CONTENTS
)
@pytest.mark.parametrize("output_to_file_flag", OUTPUT_TO_FILE_FLAGS)
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
        TEST_FILES_DIR / file_name,
        identifier_name,
        use_header_guard,
        other_arguments=(output_to_file_flag, output_file_path),
    )
    assert result.stdout == "", "Nothing written to standard output"
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"

    assert output_file_path.read_text() == get_expected_text_data_header(
        identifier_name, use_header_guard, expected_string_literal_contents
    )


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize("use_header_guard", (True, False))
@pytest.mark.parametrize(
    "file_name, expected_string_literal_contents", FILES_AND_ESCAPED_CONTENTS
)
@pytest.mark.parametrize("output_to_file_flag", OUTPUT_TO_FILE_FLAGS)
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
    file_contents = Path(TEST_FILES_DIR / file_name).read_text()
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

    assert output_file_path.read_text() == get_expected_text_data_header(
        identifier_name, use_header_guard, expected_string_literal_contents
    )
