"""Tests for the repository-publication-hygiene standard.

The rules this standard states are mechanical enough to be checked, so they
are checked here rather than trusted to the agent's memory.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest  # noqa: E402

from fixtures import load_installer  # noqa: E402

installer = load_installer()

SKILL_NAME = "repository-publication-hygiene"

#: Trailer lines that must never appear in a published commit message.
#: Matched as whole lines, so prose that merely names a trailer is allowed.
ATTRIBUTION_TRAILERS = (
    "co-authored-by",
    "signed-off-by",
    "reviewed-by",
    "generated-with",
    "created-by",
    "generated-by",
)

#: Names that identify the producing tool and must not be published.
TOOL_IDENTIFIERS = (
    "cursoragent",
    "cursor-agent",
    "claude-code",
    "copilot",
    "codeium",
    "aider",
    "devin",
)


def trailer_lines(messages: str) -> list:
    """Return the attribution-shaped lines in a commit message body.

    A trailer is a line of the form ``Key: value`` where the key is one of
    the known attribution keys. Prose that mentions the same word in the
    middle of a sentence is not a trailer and is not flagged.
    """
    found = []
    for line in messages.splitlines():
        stripped = line.strip().lower()
        for key in ATTRIBUTION_TRAILERS:
            if stripped.startswith(key + ":") or stripped.startswith(key + " :"):
                found.append(stripped)
    return found


def skill_text() -> str:
    """Return the body of the publication hygiene skill."""
    path = installer.discover_skills()[SKILL_NAME] / "SKILL.md"
    return path.read_text(encoding="utf-8")


def test_skill_exists() -> None:
    assert SKILL_NAME in installer.discover_skills()


def test_skill_is_in_every_profile() -> None:
    """Every profile must carry the standard, so it cannot be opted out of."""
    for name, path in installer.discover_profiles().items():
        _, _, skills = installer.read_profile(path)
        assert SKILL_NAME in skills, "Profile {0} omits {1}".format(name, SKILL_NAME)


def test_skill_states_the_attribution_prohibition() -> None:
    """The prohibition on tool attribution must be stated explicitly."""
    text = skill_text().lower()
    assert "co-authored-by" in text
    assert "trailer" in text


def test_skill_covers_every_published_artifact() -> None:
    """Commit metadata and history must be in scope, not just file contents."""
    text = skill_text().lower()
    for term in ("commit message", "history", "readme", "configuration"):
        assert term in text, "The standard does not mention {0}".format(term)


def test_skill_requires_scanning_history() -> None:
    """A file deleted later is still in history, so history must be scanned."""
    text = skill_text().lower()
    assert "history" in text


def test_skill_requires_empty_configuration_placeholders() -> None:
    """Example configuration must ship empty rather than filled with real values."""
    text = skill_text().lower()
    assert "placeholder" in text or "empty" in text


def test_repository_has_no_attribution_trailer_in_its_own_history() -> None:
    """The repository must follow the standard it publishes."""
    import subprocess

    result = subprocess.run(
        ["git", "log", "--format=%B"],
        cwd=str(REPO_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        pytest.skip("git history is not available")
    messages = result.stdout.decode("utf-8", errors="replace")
    found = trailer_lines(messages.lower())
    assert not found, "Commit history contains attribution trailers: {0}".format(found)


def test_trailer_detection_matches_only_trailer_lines() -> None:
    """The detector must not flag prose that merely names a trailer."""
    prose = (
        "- Forbids the agent from adding its own name to published content,\n"
        "  including Co-authored-by trailers added automatically\n"
    )
    assert trailer_lines(prose.lower()) == []


def test_trailer_detection_catches_a_real_trailer() -> None:
    """The detector must catch an actual trailer line."""
    real = "\nCo-authored-by: Cursor <cursoragent@cursor.com>\n"
    assert trailer_lines(real.lower()) == ["co-authored-by: cursor <cursoragent@cursor.com>"]


def test_repository_history_has_no_tool_identifiers() -> None:
    """The repository must follow the standard it publishes."""
    import subprocess

    result = subprocess.run(
        ["git", "log", "--format=%B"],
        cwd=str(REPO_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        pytest.skip("git history is not available")
    messages = result.stdout.decode("utf-8", errors="replace").lower()
    for identifier in TOOL_IDENTIFIERS:
        assert identifier not in messages, (
            "Commit history mentions '{0}'".format(identifier)
        )


def test_no_skill_publishes_a_home_directory_path() -> None:
    """Skills are distributed to other people's machines, so no local paths."""
    pattern = re.compile(r"/Users/[A-Za-z0-9._-]+/")
    for name, path in installer.discover_skills().items():
        text = (path / "SKILL.md").read_text(encoding="utf-8")
        assert not pattern.search(text), "{0} contains a home directory path".format(name)
