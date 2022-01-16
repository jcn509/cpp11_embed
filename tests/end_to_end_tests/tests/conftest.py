import pytest

from .cpp11_embed_path import get_cpp11_embed_path

def pytest_addoption(parser):
    print('conftest method')
    parser.addoption("--cpp11-embed-path", type=str, help ="The path to the Cpp11Embed executable", required=True)

@pytest.fixture(scope="session", autouse=True)
def _set_up_cpp11_embed_path(request):
    get_cpp11_embed_path._cpp11_embed_path = request.config.getoption("--cpp11-embed-path")