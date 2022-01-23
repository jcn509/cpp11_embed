"""Ensures that the help flag behaves as expected"""

import pytest
from .utilities import (
    FILES_AND_ESCAPED_CONTENTS,
    get_expected_text_data_header,
    run_cpp11_embed,
    TEST_FILES_DIR,
)


@pytest.mark.parametrize("identifier_name", ("test_name", "other_name"))
@pytest.mark.parametrize("use_header_guard", (True, False))
@pytest.mark.parametrize(
    "file_name, expected_string_literal_contents", FILES_AND_ESCAPED_CONTENTS
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
        TEST_FILES_DIR / file_name,
        identifier_name,
        use_header_guard,
        other_arguments=(help_flag,),
    )
    expected_header = get_expected_text_data_header(
        identifier_name, use_header_guard, expected_string_literal_contents
    )
    assert (
        "Display this help menu" in result.stdout
    ), "Help menu appears to have been displayed"
    assert expected_header not in result.stdout, "No header produced"
    assert result.stderr == "", "No errors reported"
    assert result.returncode == 0, "No errors reported"
