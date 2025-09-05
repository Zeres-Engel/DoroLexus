import os
from typing import Optional


def project_root() -> str:
    """Return absolute path to the project root directory.

    Assumes this file lives at src/core/paths.py → project root is two levels up from here.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))


def asset_path(*parts: str) -> Optional[str]:
    """Resolve an asset path by trying common bases.

    Tries these bases in order:
    1) project_root()/
    2) project_root()/src/
    3) directory of caller module (best-effort using this file as reference)
    Returns absolute path if found, else None.
    """
    candidates = [
        os.path.join(project_root(), *parts),
        os.path.join(project_root(), 'src', *parts),
        os.path.join(os.path.dirname(__file__), *([os.pardir] * 1 + list(parts))),
    ]
    for p in candidates:
        if os.path.exists(p):
            return os.path.abspath(p)
    return None


