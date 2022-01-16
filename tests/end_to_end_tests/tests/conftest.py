"""See https://www.tutorialspoint.com/pytest/pytest_conftest_py.htm"""

import pytest

from .utilities import get_cpp11_embed_path


def pytest_addoption(parser):
    """See https://docs.pytest.org/en/6.2.x/reference.html?highlight=pytest_addoption#id56"""
    print("conftest method")
    parser.addoption(
        "--cpp11-embed-path",
        type=str,
        help="The path to the Cpp11Embed executable",
        required=True,
    )


@pytest.fixture(scope="session", autouse=True)
def _set_up_cpp11_embed_path(request):
    # pylint:disable=protected-access
    get_cpp11_embed_path._cpp11_embed_path = request.config.getoption(
        "--cpp11-embed-path"
    )
