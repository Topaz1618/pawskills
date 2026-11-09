"""Shared test helpers for the Pawskills test suite."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
INSTALL_SCRIPT = REPO_ROOT / "scripts" / "install.py"


def load_installer() -> ModuleType:
    """Import scripts/install.py as a module regardless of the working directory."""
    spec = importlib.util.spec_from_file_location("pawskills_install", INSTALL_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load {0}".format(INSTALL_SCRIPT))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
