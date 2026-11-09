#!/usr/bin/env python3
"""Validate the skill files, the frontmatter, and the profile definitions.

Checks performed:

* every directory under ``skills/`` contains a ``SKILL.md``
* every ``SKILL.md`` has a well formed YAML frontmatter block
* the frontmatter declares ``name``, ``description``, and ``trigger``
* frontmatter names are unique and slug style
* every skill referenced by a profile exists
* the profile files themselves are well formed

Usage:

    python scripts/validate.py
    python scripts/validate.py --quiet
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
PROFILES_DIR = REPO_ROOT / "profiles"

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
SLUG_RE = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
REQUIRED_KEYS = ("name", "description", "trigger")

STATUS_OK = "OK"
STATUS_ERROR = "ERROR"


class ValidationError(Exception):
    """Raised for a validation failure that aborts the run."""


def parse_frontmatter(path: Path) -> dict:
    """Return the frontmatter mapping of a Markdown file."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValidationError("Could not read {0}: {1}".format(path, exc)) from exc
    match = FRONTMATTER_RE.match(text)
    if match is None:
        raise ValidationError("{0} has no YAML frontmatter block".format(path))
    return parse_yaml_mapping(match.group(1), "{0} frontmatter".format(path))


def parse_yaml_mapping(text: str, label: str) -> dict:
    """Parse a YAML mapping from a string."""
    try:
        import yaml  # type: ignore
    except ImportError:
        try:
            return _parse_simple_yaml(text)
        except ValidationError as exc:
            raise ValidationError("{0}: {1}".format(label, exc)) from exc
    try:
        data = yaml.safe_load(text)
    except Exception as exc:  # noqa: BLE001
        raise ValidationError("Could not parse {0}: {1}".format(label, exc)) from exc
    if not isinstance(data, dict):
        raise ValidationError("{0} is not a mapping".format(label))
    return data


def parse_yaml_file(path: Path) -> dict:
    """Return the mapping of a plain YAML file."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValidationError("Could not read {0}: {1}".format(path, exc)) from exc
    return parse_yaml_mapping(text, str(path))


def _parse_simple_yaml(text: str) -> dict:
    """Parse the small YAML subset used by the frontmatter and profile files."""
    result: dict = {}
    current_key: Optional[str] = None
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.strip().startswith("#"):
            continue
        stripped = raw_line.split("#", 1)[0].strip()
        if not stripped:
            continue
        if stripped.startswith("- "):
            if current_key is None:
                raise ValidationError("List item without a parent key.")
            items = result.setdefault(current_key, [])
            if not isinstance(items, list):
                raise ValidationError("Conflicting definition for '{0}'.".format(current_key))
            items.append(stripped[2:].strip().strip('"').strip("'"))
            continue
        if ":" not in stripped:
            raise ValidationError("Malformed line: {0}".format(raw_line.rstrip()))
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()
        if value == "":
            result[key] = []
            current_key = key
        else:
            result[key] = value.strip('"').strip("'")
            current_key = None
    return result


def check_skills() -> List[str]:
    """Validate every skill file. Returns a list of error messages."""
    errors: List[str] = []
    if not SKILLS_DIR.is_dir():
        return ["Skills directory not found: {0}".format(SKILLS_DIR)]

    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    if not skill_dirs:
        return ["No skill directories found in {0}".format(SKILLS_DIR)]

    seen_names = {}
    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append("{0}: SKILL.md is missing".format(skill_dir.name))
            continue
        if not skill_file.read_text(encoding="utf-8").strip():
            errors.append("{0}: SKILL.md is empty".format(skill_dir.name))
            continue
        try:
            data = parse_frontmatter(skill_file)
        except ValidationError as exc:
            errors.append(str(exc))
            continue

        for key in REQUIRED_KEYS:
            if key not in data:
                errors.append("{0}: frontmatter is missing '{1}'".format(skill_dir.name, key))
            elif not isinstance(data[key], str) or not data[key].strip():
                errors.append("{0}: frontmatter '{1}' is empty or not a string".format(skill_dir.name, key))

        name = data.get("name")
        if isinstance(name, str) and name.strip():
            if not SLUG_RE.fullmatch(name.strip()):
                errors.append("{0}: frontmatter name '{1}' is not slug style".format(skill_dir.name, name))
            if name in seen_names:
                errors.append(
                    "{0}: frontmatter name '{1}' duplicates {2}".format(
                        skill_dir.name, name, seen_names[name]
                    )
                )
            else:
                seen_names[name] = skill_dir.name

        body = FRONTMATTER_RE.sub("", skill_file.read_text(encoding="utf-8"), count=1)
        if not re.search(r"^#\s+\S", body, re.MULTILINE):
            errors.append("{0}: body has no top-level heading".format(skill_dir.name))
    return errors


def check_profiles() -> List[str]:
    """Validate every profile file. Returns a list of error messages."""
    errors: List[str] = []
    if not PROFILES_DIR.is_dir():
        return ["Profiles directory not found: {0}".format(PROFILES_DIR)]

    profile_files = sorted(PROFILES_DIR.glob("*.yaml"))
    if not profile_files:
        return ["No profile files found in {0}".format(PROFILES_DIR)]

    skill_names = {p.name for p in SKILLS_DIR.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()}

    for profile_file in profile_files:
        try:
            data = parse_yaml_file(profile_file)
        except ValidationError as exc:
            errors.append(str(exc))
            continue
        if "name" not in data or not str(data.get("name", "")).strip():
            errors.append("{0}: missing 'name'".format(profile_file.name))
        if "description" not in data or not str(data.get("description", "")).strip():
            errors.append("{0}: missing 'description'".format(profile_file.name))
        skills = data.get("skills")
        if not isinstance(skills, list) or not skills:
            errors.append("{0}: 'skills' must be a non-empty list".format(profile_file.name))
            continue
        for skill in skills:
            if str(skill) not in skill_names:
                errors.append(
                    "{0}: references unknown skill '{1}'".format(profile_file.name, skill)
                )
    return errors


def run(quiet: bool = False) -> int:
    """Run all checks. Returns 0 when everything is valid, 1 otherwise."""
    results: List[Tuple[str, List[str]]] = [
        ("skills", check_skills()),
        ("profiles", check_profiles()),
    ]

    total_errors = 0
    for label, errors in results:
        total_errors += len(errors)
        if quiet:
            continue
        if errors:
            for message in errors:
                print("[{0}] {1}: {2}".format(STATUS_ERROR, label, message))
        else:
            print("[{0}] {1}: no problems found".format(STATUS_OK, label))

    if total_errors == 0:
        print("")
        print("Validation passed.")
        return 0
    print("")
    print("Validation failed with {0} error(s).".format(total_errors))
    return 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="validate.py",
        description="Validate the skill files, the frontmatter, and the profile definitions.",
    )
    parser.add_argument("--quiet", action="store_true", help="Only print the final result.")
    args = parser.parse_args(argv)
    try:
        return run(quiet=args.quiet)
    except ValidationError as exc:
        print("[{0}] {1}".format(STATUS_ERROR, exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
