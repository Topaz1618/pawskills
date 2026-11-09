"""Tests for scripts/install.py.

Every test runs against a temporary directory. The real user project and the
real user home skills directory are never modified.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixtures import load_installer  # noqa: E402

installer = load_installer()


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    target = tmp_path / "project"
    target.mkdir()
    return target


def run(argv, expect_success=True):
    """Run the installer CLI and return the exit code."""
    code = installer.main([str(a) for a in argv])
    if expect_success:
        assert code == 0, "installer returned {0}".format(code)
    return code


# --------------------------------------------------------------------------- #
# Target resolution
# --------------------------------------------------------------------------- #


def test_claude_code_project_scope(project: Path) -> None:
    target = installer.resolve_target("claude-code", "project", project)
    assert target == (project / ".claude" / "skills").resolve()


def test_claude_code_user_scope(project: Path) -> None:
    target = installer.resolve_target("claude-code", "user", project)
    assert target == (Path.home() / ".claude" / "skills").resolve()


def test_codex_project_scope(project: Path) -> None:
    target = installer.resolve_target("codex", "project", project)
    assert target == (project / ".agents" / "skills").resolve()


def test_codex_user_scope(project: Path) -> None:
    target = installer.resolve_target("codex", "user", project)
    assert target == (Path.home() / ".agents" / "skills").resolve()


def test_unknown_agent_is_rejected(project: Path) -> None:
    with pytest.raises(installer.InstallError):
        installer.resolve_target("unknown-agent", "project", project)


def test_unknown_scope_is_rejected(project: Path) -> None:
    with pytest.raises(installer.InstallError):
        installer.resolve_target("codex", "global", project)


# --------------------------------------------------------------------------- #
# Profile and skill selection
# --------------------------------------------------------------------------- #


def test_invalid_profile_is_rejected(project: Path) -> None:
    code = run(
        ["--agent", "codex", "--profile", "does-not-exist", "--project-dir", str(project)],
        expect_success=False,
    )
    assert code == 1


def test_invalid_skill_name_is_rejected(project: Path) -> None:
    code = run(
        ["--agent", "codex", "--skill", "no-such-skill", "--project-dir", str(project)],
        expect_success=False,
    )
    assert code == 1


def test_select_skill_names_deduplicates() -> None:
    profiles = installer.discover_profiles()
    names = installer.select_skill_names("lightweight", ["task-execution-governance"], profiles)
    assert names.count("task-execution-governance") == 1


def test_select_skill_names_requires_something() -> None:
    profiles = installer.discover_profiles()
    with pytest.raises(installer.InstallError):
        installer.select_skill_names(None, [], profiles)


# --------------------------------------------------------------------------- #
# Profile installation
# --------------------------------------------------------------------------- #


def test_profile_install_creates_all_skills(project: Path) -> None:
    run(["--agent", "codex", "--profile", "lightweight", "--project-dir", str(project)])
    root = project / ".agents" / "skills"
    for skill in ("task-execution-governance", "testing-verification", "unfinished-work-tracking"):
        assert (root / skill / "SKILL.md").is_file()


def test_claude_code_profile_install(project: Path) -> None:
    run(["--agent", "claude-code", "--profile", "lightweight", "--project-dir", str(project)])
    root = project / ".claude" / "skills"
    assert (root / "task-execution-governance" / "SKILL.md").is_file()


def test_codex_profile_install(project: Path) -> None:
    run(["--agent", "codex", "--profile", "lightweight", "--project-dir", str(project)])
    root = project / ".agents" / "skills"
    assert (root / "task-execution-governance" / "SKILL.md").is_file()


def test_user_scope_targets_home(project: Path, monkeypatch) -> None:
    home = project / "home"
    home.mkdir()
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    run(["--agent", "codex", "--profile", "lightweight", "--scope", "user", "--project-dir", str(project)])
    assert (home / ".agents" / "skills" / "task-execution-governance" / "SKILL.md").is_file()


def test_installed_content_matches_source(project: Path) -> None:
    run(["--agent", "codex", "--skill", "production-logging", "--project-dir", str(project)])
    source = installer.SKILLS_DIR / "production-logging" / "SKILL.md"
    installed = project / ".agents" / "skills" / "production-logging" / "SKILL.md"
    assert installed.read_text(encoding="utf-8") == source.read_text(encoding="utf-8")


def test_manifest_records_installed_skill(project: Path) -> None:
    run(["--agent", "codex", "--skill", "production-logging", "--project-dir", str(project)])
    manifest_path = project / ".agents" / "skills" / installer.MANIFEST_NAME
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert "production-logging" in manifest["skills"]
    entry = manifest["skills"]["production-logging"]
    assert any(f["path"] == "SKILL.md" for f in entry["files"])


# --------------------------------------------------------------------------- #
# Conflict handling
# --------------------------------------------------------------------------- #


def test_existing_skill_is_skipped_without_force(project: Path) -> None:
    root = project / ".agents" / "skills" / "production-logging"
    root.mkdir(parents=True)
    (root / "SKILL.md").write_text("user content", encoding="utf-8")

    run(["--agent", "codex", "--skill", "production-logging", "--project-dir", str(project)])

    assert (root / "SKILL.md").read_text(encoding="utf-8") == "user content"


def test_force_overwrites_existing_skill(project: Path) -> None:
    root = project / ".agents" / "skills" / "production-logging"
    root.mkdir(parents=True)
    (root / "SKILL.md").write_text("user content", encoding="utf-8")

    run(["--agent", "codex", "--skill", "production-logging", "--force", "--project-dir", str(project)])

    assert "user content" not in (root / "SKILL.md").read_text(encoding="utf-8")


def test_force_backs_up_previous_version(project: Path) -> None:
    root = project / ".agents" / "skills" / "production-logging"
    root.mkdir(parents=True)
    (root / "SKILL.md").write_text("user content", encoding="utf-8")

    run(["--agent", "codex", "--skill", "production-logging", "--force", "--project-dir", str(project)])

    backups = list((project / ".agents" / "skills" / installer.BACKUP_DIR_NAME).rglob("SKILL.md"))
    assert backups, "no backup was created"
    assert backups[0].read_text(encoding="utf-8") == "user content"


def test_conflict_does_not_block_other_skills(project: Path) -> None:
    root = project / ".agents" / "skills" / "production-logging"
    root.mkdir(parents=True)
    (root / "SKILL.md").write_text("user content", encoding="utf-8")

    run(
        [
            "--agent",
            "codex",
            "--skill",
            "production-logging",
            "--skill",
            "testing-verification",
            "--project-dir",
            str(project),
        ]
    )

    assert (root / "SKILL.md").read_text(encoding="utf-8") == "user content"
    assert (project / ".agents" / "skills" / "testing-verification" / "SKILL.md").is_file()


# --------------------------------------------------------------------------- #
# Dry run
# --------------------------------------------------------------------------- #


def test_dry_run_creates_nothing(project: Path) -> None:
    run(
        ["--agent", "codex", "--profile", "lightweight", "--dry-run", "--project-dir", str(project)]
    )
    assert not (project / ".agents").exists()


def test_dry_run_does_not_overwrite(project: Path) -> None:
    root = project / ".agents" / "skills" / "production-logging"
    root.mkdir(parents=True)
    (root / "SKILL.md").write_text("user content", encoding="utf-8")

    run(
        [
            "--agent",
            "codex",
            "--skill",
            "production-logging",
            "--force",
            "--dry-run",
            "--project-dir",
            str(project),
        ]
    )

    assert (root / "SKILL.md").read_text(encoding="utf-8") == "user content"


# --------------------------------------------------------------------------- #
# Uninstall
# --------------------------------------------------------------------------- #


def test_uninstall_removes_managed_skills(project: Path) -> None:
    run(["--agent", "codex", "--skill", "production-logging", "--project-dir", str(project)])
    run(
        [
            "--agent",
            "codex",
            "--skill",
            "production-logging",
            "--uninstall",
            "--project-dir",
            str(project),
        ]
    )
    assert not (project / ".agents" / "skills" / "production-logging").exists()


def test_uninstall_leaves_unmanaged_skills(project: Path) -> None:
    root = project / ".agents" / "skills" / "my-own-skill"
    root.mkdir(parents=True)
    (root / "SKILL.md").write_text("mine", encoding="utf-8")

    run(
        [
            "--agent",
            "codex",
            "--skill",
            "my-own-skill",
            "--uninstall",
            "--project-dir",
            str(project),
        ]
    )

    assert (root / "SKILL.md").is_file()


def test_uninstall_protects_user_modified_files(project: Path) -> None:
    run(["--agent", "codex", "--skill", "production-logging", "--project-dir", str(project)])
    skill_file = project / ".agents" / "skills" / "production-logging" / "SKILL.md"
    skill_file.write_text("edited by user", encoding="utf-8")

    run(
        [
            "--agent",
            "codex",
            "--skill",
            "production-logging",
            "--uninstall",
            "--project-dir",
            str(project),
        ]
    )

    assert skill_file.is_file()
    assert skill_file.read_text(encoding="utf-8") == "edited by user"


def test_uninstall_with_force_removes_modified_files(project: Path) -> None:
    run(["--agent", "codex", "--skill", "production-logging", "--project-dir", str(project)])
    skill_file = project / ".agents" / "skills" / "production-logging" / "SKILL.md"
    skill_file.write_text("edited by user", encoding="utf-8")

    run(
        [
            "--agent",
            "codex",
            "--skill",
            "production-logging",
            "--uninstall",
            "--force",
            "--project-dir",
            str(project),
        ]
    )

    assert not skill_file.exists()


def test_uninstall_dry_run_keeps_files(project: Path) -> None:
    run(["--agent", "codex", "--skill", "production-logging", "--project-dir", str(project)])
    run(
        [
            "--agent",
            "codex",
            "--skill",
            "production-logging",
            "--uninstall",
            "--dry-run",
            "--project-dir",
            str(project),
        ]
    )
    assert (project / ".agents" / "skills" / "production-logging" / "SKILL.md").is_file()


def test_uninstall_without_manifest_is_a_no_op(project: Path) -> None:
    code = run(
        ["--agent", "codex", "--skill", "production-logging", "--uninstall", "--project-dir", str(project)]
    )
    assert code == 0


# --------------------------------------------------------------------------- #
# Listing
# --------------------------------------------------------------------------- #


def test_list_runs_successfully(capsys) -> None:
    run(["--list"])
    output = capsys.readouterr().out
    assert "production-logging" in output
    assert "lightweight" in output


def test_agent_is_required(capsys) -> None:
    code = run(["--profile", "full"], expect_success=False)
    assert code == 1
