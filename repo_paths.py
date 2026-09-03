from __future__ import annotations

import os
import sys
from pathlib import Path


def resolve_repo_root(start_path: Path | None = None) -> Path:
    env_root = os.getenv("MODELLING_CORTEX_REPO_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()

    search_start = Path(start_path or Path.cwd()).resolve()
    if search_start.is_file():
        search_start = search_start.parent

    for candidate in (search_start, *search_start.parents):
        if (candidate / ".git").exists() or (candidate / "README.md").exists():
            return candidate

    raise RuntimeError("Could not resolve repository root; set MODELLING_CORTEX_REPO_ROOT.")


def ensure_repo_on_syspath(repo_root: Path) -> None:
    repo_root_str = str(repo_root)
    if repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)
