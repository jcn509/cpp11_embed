from pathlib import Path

def get_cpp11_embed_path() -> str:
    if get_cpp11_embed_path._cpp11_embed_path is None:
        raise RuntimeError("Path not set up yet")
    return get_cpp11_embed_path._cpp11_embed_path
get_cpp11_embed_path._cpp11_embed_path = None