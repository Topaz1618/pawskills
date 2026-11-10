"""Tests for the skill directory structure and the profile definitions."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixtures import load_installer  # noqa: E402

installer = load_installer()

EXPECTED_SKILLS = {
    "task-execution-governance",
    "user-intent-priority",
    "data-first-execution",
    "code-asset-inventory",
    "interface-contract",
    "data-audit-reproducibility",
    "production-logging",
    "testing-verification",
    "engineering-transparency",
    "technical-documentation",
    "documentation-structure",
    "language-expression",
    "change-report-delivery",
    "unfinished-work-tracking",
    "explicit-instruction-fidelity",
}

EXPECTED_PROFILES = {"full", "development", "data", "lightweight"}


def test_skills_directory_exists() -> None:
    assert (REPO_ROOT / "skills").is_dir()


def test_all_expected_skills_present() -> None:
    discovered = installer.discover_skills()
    missing = EXPECTED_SKILLS - set(discovered)
    assert not missing, "Missing skills: {0}".format(sorted(missing))


def test_every_skill_has_skill_md() -> None:
    for name, path in installer.discover_skills().items():
        assert (path / "SKILL.md").is_file(), "{0} has no SKILL.md".format(name)


def test_every_skill_file_is_not_empty() -> None:
    for name, path in installer.discover_skills().items():
        content = (path / "SKILL.md").read_text(encoding="utf-8")
        assert content.strip(), "{0} SKILL.md is empty".format(name)


def test_all_expected_profiles_present() -> None:
    discovered = installer.discover_profiles()
    missing = EXPECTED_PROFILES - set(discovered)
    assert not missing, "Missing profiles: {0}".format(sorted(missing))


def test_profile_skills_all_exist() -> None:
    skills = installer.discover_skills()
    for profile_name, path in installer.discover_profiles().items():
        _, _, profile_skills = installer.read_profile(path)
        unknown = [s for s in profile_skills if s not in skills]
        assert not unknown, "Profile {0} references unknown skills: {1}".format(profile_name, unknown)


def test_full_profile_contains_every_expected_skill() -> None:
    profiles = installer.discover_profiles()
    _, _, profile_skills = installer.read_profile(profiles["full"])
    assert set(profile_skills) == EXPECTED_SKILLS


def test_each_profile_has_description_and_name() -> None:
    for profile_name, path in installer.discover_profiles().items():
        name, description, _ = installer.read_profile(path)
        assert name, "Profile {0} has no name".format(profile_name)
        assert description, "Profile {0} has no description".format(profile_name)


def test_lightweight_profile_is_a_subset_of_full() -> None:
    profiles = installer.discover_profiles()
    _, _, full_skills = installer.read_profile(profiles["full"])
    _, _, light_skills = installer.read_profile(profiles["lightweight"])
    assert set(light_skills).issubset(set(full_skills))


def test_data_profile_contains_data_standards() -> None:
    profiles = installer.discover_profiles()
    _, _, data_skills = installer.read_profile(profiles["data"])
    assert "data-audit-reproducibility" in data_skills
    assert "data-first-execution" in data_skills
    assert "production-logging" in data_skills


def test_read_profile_rejects_empty_skill_list(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("name: bad\ndescription: nothing\nskills: []\n", encoding="utf-8")
    with pytest.raises(installer.InstallError):
        installer.read_profile(bad)


def test_read_profile_rejects_missing_skills_key(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("name: bad\ndescription: nothing\n", encoding="utf-8")
    with pytest.raises(installer.InstallError):
        installer.read_profile(bad)
