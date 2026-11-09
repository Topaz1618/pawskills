"""Tests for the YAML frontmatter of every skill file."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixtures import load_installer  # noqa: E402

installer = load_installer()

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter(path: Path) -> dict:
    """Return the frontmatter mapping of a Markdown file."""
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if match is None:
        raise AssertionError("{0} has no YAML frontmatter block".format(path))
    data = installer.load_yaml_from_text(match.group(1))
    return data


@pytest.fixture(params=sorted(installer.discover_skills().items()), ids=lambda item: item[0])
def skill_item(request) -> tuple:
    return request.param


def test_frontmatter_block_exists(skill_item) -> None:
    name, path = skill_item
    text = (path / "SKILL.md").read_text(encoding="utf-8")
    assert FRONTMATTER_RE.match(text), "{0} has no frontmatter".format(name)


def test_frontmatter_has_required_keys(skill_item) -> None:
    name, path = skill_item
    data = parse_frontmatter(path / "SKILL.md")
    for key in ("name", "description", "trigger"):
        assert key in data, "{0} frontmatter is missing '{1}'".format(name, key)


def test_frontmatter_values_are_non_empty_strings(skill_item) -> None:
    name, path = skill_item
    data = parse_frontmatter(path / "SKILL.md")
    for key in ("name", "description", "trigger"):
        value = data[key]
        assert isinstance(value, str), "{0} frontmatter '{1}' is not a string".format(name, key)
        assert value.strip(), "{0} frontmatter '{1}' is empty".format(name, key)


def test_frontmatter_names_are_unique(skill_item) -> None:
    seen = {}
    for name, path in installer.discover_skills().items():
        data = parse_frontmatter(path / "SKILL.md")
        frontmatter_name = data["name"]
        assert frontmatter_name not in seen, (
            "Duplicate frontmatter name '{0}' in {1} and {2}".format(
                frontmatter_name, seen.get(frontmatter_name), name
            )
        )
        seen[frontmatter_name] = name


def test_frontmatter_names_are_slug_style(skill_item) -> None:
    name, path = skill_item
    data = parse_frontmatter(path / "SKILL.md")
    assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", data["name"]), (
        "{0} frontmatter name '{1}' is not slug style".format(name, data["name"])
    )


def test_body_contains_a_heading(skill_item) -> None:
    name, path = skill_item
    text = (path / "SKILL.md").read_text(encoding="utf-8")
    body = FRONTMATTER_RE.sub("", text, count=1)
    assert re.search(r"^#\s+\S", body, re.MULTILINE), "{0} has no top-level heading".format(name)
