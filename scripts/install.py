#!/usr/bin/env python3
"""Install, verify, and uninstall the Agent Engineering Standards skills.

The installer reads its skill inventory from the ``profiles/`` YAML files and the
``skills/`` directory. Nothing about the skill list is hardcoded here: the
profile files are the single source of truth for what a profile installs.

Supported agents:

    claude-code   project: .claude/skills/    user: ~/.claude/skills/
    codex         project: .agents/skills/    user: ~/.agents/skills/

Usage examples:

    python scripts/install.py --list
    python scripts/install.py --agent codex --profile full
    python scripts/install.py --agent claude-code --profile full --scope user
    python scripts/install.py --agent codex --skill production-logging
    python scripts/install.py --agent codex --profile full --dry-run
    python scripts/install.py --agent codex --profile full --uninstall
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
PROFILES_DIR = REPO_ROOT / "profiles"

MANIFEST_NAME = ".pawskills-manifest.json"
BACKUP_DIR_NAME = ".pawskills-backups"

STATUS_SUCCESS = "SUCCESS"
STATUS_SKIPPED = "SKIPPED"
STATUS_FAILED = "FAILED"
STATUS_WARNING = "WARNING"

# agent key -> (project relative skills dir, user relative skills dir)
AGENTS: Dict[str, Tuple[str, str]] = {
    "claude-code": (".claude/skills", ".claude/skills"),
    "codex": (".agents/skills", ".agents/skills"),
}


class InstallError(Exception):
    """Raised for user-facing errors that abort the current operation."""


# --------------------------------------------------------------------------- #
# Output helpers
# --------------------------------------------------------------------------- #


def emit(status: str, message: str) -> None:
    """Print one structured status line. No emoji are used as status markers."""
    print("[{0}] {1}".format(status, message))


def section(title: str) -> None:
    print("")
    print("== {0} ==".format(title))


# --------------------------------------------------------------------------- #
# YAML loading
# --------------------------------------------------------------------------- #


def _parse_simple_yaml(text: str) -> Dict[str, object]:
    """Parse the small YAML subset used by the profile files.

    Supports a top level mapping, scalar values, and block sequences of
    scalars. Used only when PyYAML is not installed.
    """
    result: Dict[str, object] = {}
    current_key: Optional[str] = None
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip() if not raw_line.strip().startswith("#") else ""
        if not line.strip():
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            if current_key is None:
                raise InstallError("Malformed YAML: list item without a parent key.")
            items = result.setdefault(current_key, [])
            if not isinstance(items, list):
                raise InstallError("Malformed YAML: conflicting definition for '{0}'.".format(current_key))
            items.append(stripped[2:].strip().strip('"').strip("'"))
            continue
        if ":" not in stripped:
            raise InstallError("Malformed YAML line: {0}".format(raw_line.rstrip()))
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


def load_yaml_from_text(text: str) -> Dict[str, object]:
    """Parse a YAML mapping from a string, using PyYAML when it is available."""
    try:
        import yaml  # type: ignore
    except ImportError:
        return _parse_simple_yaml(text)
    try:
        data = yaml.safe_load(text)
    except Exception as exc:  # noqa: BLE001 - surfaced to the user verbatim
        raise InstallError("Could not parse YAML: {0}".format(exc)) from exc
    if not isinstance(data, dict):
        raise InstallError("YAML content must be a mapping.")
    return data


def load_yaml(path: Path) -> Dict[str, object]:
    """Load a YAML mapping from disk, using PyYAML when it is available."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise InstallError("Could not read {0}: {1}".format(path, exc)) from exc
    return load_yaml_from_text(text)


# --------------------------------------------------------------------------- #
# Repository inventory
# --------------------------------------------------------------------------- #


def discover_skills() -> Dict[str, Path]:
    """Return every skill directory that contains a SKILL.md file."""
    if not SKILLS_DIR.is_dir():
        raise InstallError("Skills directory not found: {0}".format(SKILLS_DIR))
    found: Dict[str, Path] = {}
    for entry in sorted(SKILLS_DIR.iterdir()):
        if entry.is_dir() and (entry / "SKILL.md").is_file():
            found[entry.name] = entry
    return found


def discover_profiles() -> Dict[str, Path]:
    """Return every profile YAML file keyed by its file stem."""
    if not PROFILES_DIR.is_dir():
        raise InstallError("Profiles directory not found: {0}".format(PROFILES_DIR))
    return {entry.stem: entry for entry in sorted(PROFILES_DIR.glob("*.yaml"))}


def read_profile(profile_path: Path) -> Tuple[str, str, List[str]]:
    """Read a profile and return its name, description, and skill list."""
    data = load_yaml(profile_path)
    name = str(data.get("name") or profile_path.stem)
    description = str(data.get("description") or "")
    raw_skills = data.get("skills")
    if not isinstance(raw_skills, list) or not raw_skills:
        raise InstallError("Profile {0} does not declare a non-empty 'skills' list.".format(profile_path.name))
    skills = [str(item).strip() for item in raw_skills if str(item).strip()]
    return name, description, skills


# --------------------------------------------------------------------------- #
# Hashing and manifests
# --------------------------------------------------------------------------- #


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_skill_files(skill_dir: Path) -> List[Path]:
    """Return every file inside a skill directory, relative paths sorted."""
    files: List[Path] = []
    for path in skill_dir.rglob("*"):
        if path.is_file():
            files.append(path.relative_to(skill_dir))
    return sorted(files)


def manifest_path(target_root: Path) -> Path:
    return target_root / MANIFEST_NAME


def load_manifest(target_root: Path) -> Dict[str, object]:
    path = manifest_path(target_root)
    if not path.is_file():
        return {"version": 1, "skills": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise InstallError("Could not read manifest {0}: {1}".format(path, exc)) from exc
    if not isinstance(data, dict):
        raise InstallError("Manifest {0} is malformed.".format(path))
    data.setdefault("skills", {})
    return data


def save_manifest(target_root: Path, manifest: Dict[str, object]) -> None:
    target_root.mkdir(parents=True, exist_ok=True)
    path = manifest_path(target_root)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# Target resolution
# --------------------------------------------------------------------------- #


def resolve_target(agent: str, scope: str, project_dir: Path) -> Path:
    """Return the skills directory for the given agent and scope."""
    if agent not in AGENTS:
        raise InstallError(
            "Unknown agent '{0}'. Supported agents: {1}.".format(agent, ", ".join(sorted(AGENTS)))
        )
    if scope not in ("project", "user"):
        raise InstallError("Unknown scope '{0}'. Supported scopes: project, user.".format(scope))
    project_rel, user_rel = AGENTS[agent]
    if scope == "project":
        return (project_dir / project_rel).resolve()
    return (Path.home() / user_rel).resolve()


# --------------------------------------------------------------------------- #
# Planning
# --------------------------------------------------------------------------- #


class SkillPlan:
    """A single skill that the installer intends to install."""

    def __init__(self, name: str, source: Path, target: Path) -> None:
        self.name = name
        self.source = source
        self.target = target
        self.existing_files: List[Path] = []
        self.conflict = False
        self.reason = ""

    @property
    def target_exists(self) -> bool:
        return self.target.exists()


def build_plans(skill_names: Sequence[str], skills: Dict[str, Path], target_root: Path) -> List[SkillPlan]:
    """Resolve skill names into concrete install plans."""
    plans: List[SkillPlan] = []
    seen: set = set()
    for name in skill_names:
        if name in seen:
            continue
        seen.add(name)
        source = skills.get(name)
        if source is None:
            raise InstallError(
                "Skill '{0}' does not exist in {1}. Available: {2}.".format(
                    name, SKILLS_DIR, ", ".join(sorted(skills))
                )
            )
        plan = SkillPlan(name, source, target_root / name)
        if plan.target_exists:
            plan.conflict = True
            plan.reason = "target directory already exists"
            plan.existing_files = [p for p in plan.target.rglob("*") if p.is_file()]
        plans.append(plan)
    return plans


def select_skill_names(
    profile_name: Optional[str],
    skill_names: Sequence[str],
    profiles: Dict[str, Path],
) -> List[str]:
    """Resolve the requested profile and/or skills into a single skill list."""
    selected: List[str] = []
    if profile_name:
        if profile_name not in profiles:
            raise InstallError(
                "Unknown profile '{0}'. Available profiles: {1}.".format(
                    profile_name, ", ".join(sorted(profiles))
                )
            )
        _, _, profile_skills = read_profile(profiles[profile_name])
        selected.extend(profile_skills)
    selected.extend(skill_names)
    if not selected:
        raise InstallError(
            "Nothing to install. Use --profile, --skill, or --list to see the available options."
        )
    ordered: List[str] = []
    for name in selected:
        if name not in ordered:
            ordered.append(name)
    return ordered


# --------------------------------------------------------------------------- #
# Install
# --------------------------------------------------------------------------- #


def backup_existing(plan: SkillPlan, target_root: Path) -> Optional[Path]:
    """Copy an existing skill directory into the backup area."""
    if not plan.target.exists():
        return None
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = target_root / BACKUP_DIR_NAME / "{0}-{1}".format(plan.name, stamp)
    backup_root.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(plan.target, backup_root)
    return backup_root


def install_skill(plan: SkillPlan, target_root: Path, manifest: Dict[str, object]) -> None:
    """Copy one skill directory into the target and record it in the manifest."""
    plan.target.parent.mkdir(parents=True, exist_ok=True)
    if plan.target.exists():
        shutil.rmtree(plan.target)
    shutil.copytree(plan.source, plan.target)

    files = []
    for relative in iter_skill_files(plan.target):
        files.append({"path": relative.as_posix(), "sha256": file_sha256(plan.target / relative)})

    skills = manifest.setdefault("skills", {})
    assert isinstance(skills, dict)
    skills[plan.name] = {
        "source": str(plan.source),
        "installed_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "files": files,
    }


def verify_installed_skill(plan: SkillPlan) -> List[str]:
    """Check that the installed skill is complete. Returns a list of problems."""
    problems: List[str] = []
    if not plan.target.is_dir():
        problems.append("target directory is missing")
        return problems
    skill_file = plan.target / "SKILL.md"
    if not skill_file.is_file():
        problems.append("SKILL.md is missing")
        return problems
    expected = iter_skill_files(plan.source)
    actual = iter_skill_files(plan.target)
    if expected != actual:
        problems.append(
            "file set differs: expected {0} file(s), found {1}".format(len(expected), len(actual))
        )
    for relative in expected:
        source_file = plan.source / relative
        target_file = plan.target / relative
        if not target_file.is_file():
            problems.append("missing file: {0}".format(relative.as_posix()))
            continue
        if file_sha256(source_file) != file_sha256(target_file):
            problems.append("content mismatch: {0}".format(relative.as_posix()))
    return problems


def run_install(
    agent: str,
    scope: str,
    project_dir: Path,
    profile_name: Optional[str],
    skill_names: Sequence[str],
    force: bool,
    dry_run: bool,
) -> int:
    profiles = discover_profiles()
    skills = discover_skills()
    names = select_skill_names(profile_name, skill_names, profiles)
    target_root = resolve_target(agent, scope, project_dir)
    plans = build_plans(names, skills, target_root)

    section("Plan")
    print("Agent:   {0}".format(agent))
    print("Scope:   {0}".format(scope))
    print("Target:  {0}".format(target_root))
    print("Profile: {0}".format(profile_name or "(none)"))
    print("Skills:  {0}".format(len(plans)))

    section("Skills")
    for plan in plans:
        print("  {0}".format(plan.name))
        print("    source: {0}".format(plan.source))
        print("    target: {0}".format(plan.target))
        if plan.conflict:
            print("    conflict: {0}".format(plan.reason))
            for existing in plan.existing_files:
                print("      existing file: {0}".format(existing))

    if dry_run:
        section("Dry Run")
        print("No files were created, modified, or deleted.")
        return 0

    manifest = load_manifest(target_root)
    installed: List[SkillPlan] = []
    skipped = 0
    failed = 0

    section("Install")
    for plan in plans:
        if plan.conflict and not force:
            emit(
                STATUS_SKIPPED,
                "{0}: skipped, target already exists (use --force to overwrite)".format(plan.name),
            )
            skipped += 1
            continue
        try:
            if plan.conflict and force:
                backup = backup_existing(plan, target_root)
                if backup is not None:
                    emit(
                        STATUS_WARNING,
                        "{0}: previous version backed up to {1}".format(plan.name, backup),
                    )
            install_skill(plan, target_root, manifest)
        except (OSError, shutil.Error) as exc:
            emit(STATUS_FAILED, "{0}: {1}".format(plan.name, exc))
            failed += 1
            continue
        emit(STATUS_SUCCESS, "{0}: installed to {1}".format(plan.name, plan.target))
        installed.append(plan)

    save_manifest(target_root, manifest)

    section("Verification")
    for plan in installed:
        problems = verify_installed_skill(plan)
        if problems:
            emit(STATUS_FAILED, "{0}: {1}".format(plan.name, "; ".join(problems)))
            failed += 1
        else:
            emit(STATUS_SUCCESS, "{0}: verified".format(plan.name))

    section("Summary")
    print("Installed: {0}".format(len(installed)))
    print("Skipped:   {0}".format(skipped))
    print("Failed:    {0}".format(failed))
    print("Manifest:  {0}".format(manifest_path(target_root)))
    return 1 if failed else 0


# --------------------------------------------------------------------------- #
# Uninstall
# --------------------------------------------------------------------------- #


def run_uninstall(
    agent: str,
    scope: str,
    project_dir: Path,
    profile_name: Optional[str],
    skill_names: Sequence[str],
    force: bool,
    dry_run: bool,
) -> int:
    profiles = discover_profiles()
    skills = discover_skills()
    names = select_skill_names(profile_name, skill_names, profiles)
    target_root = resolve_target(agent, scope, project_dir)

    if not manifest_path(target_root).is_file():
        emit(
            STATUS_WARNING,
            "No Pawskills manifest found at {0}; nothing to uninstall.".format(target_root),
        )
        return 0

    manifest = load_manifest(target_root)
    manifest_skills = manifest.get("skills", {})
    if not isinstance(manifest_skills, dict):
        emit(STATUS_FAILED, "Manifest {0} is malformed.".format(manifest_path(target_root)))
        return 1

    section("Plan")
    print("Agent:   {0}".format(agent))
    print("Scope:   {0}".format(scope))
    print("Target:  {0}".format(target_root))
    for name in names:
        entry = manifest_skills.get(name)
        if entry is None:
            print("  {0}: not installed by Pawskills".format(name))
        else:
            print("  {0}: managed by Pawskills".format(name))

    if dry_run:
        section("Dry Run")
        print("No files were created, modified, or deleted.")
        return 0

    removed = 0
    skipped = 0
    failed = 0

    section("Uninstall")
    for name in names:
        entry = manifest_skills.get(name)
        if entry is None:
            emit(STATUS_SKIPPED, "{0}: not installed by Pawskills, left untouched".format(name))
            skipped += 1
            continue
        skill_dir = target_root / name
        files = entry.get("files", []) if isinstance(entry, dict) else []
        modified: List[str] = []
        for record in files:
            if not isinstance(record, dict):
                continue
            relative = Path(str(record.get("path", "")))
            expected = str(record.get("sha256", ""))
            target_file = skill_dir / relative
            if not target_file.is_file():
                continue
            if expected and file_sha256(target_file) != expected:
                modified.append(relative.as_posix())

        if modified and not force:
            emit(
                STATUS_SKIPPED,
                "{0}: modified after installation ({1}); use --force to remove anyway".format(
                    name, ", ".join(modified)
                ),
            )
            skipped += 1
            continue

        try:
            if skill_dir.exists():
                shutil.rmtree(skill_dir)
        except (OSError, shutil.Error) as exc:
            emit(STATUS_FAILED, "{0}: {1}".format(name, exc))
            failed += 1
            continue
        manifest_skills.pop(name, None)
        emit(STATUS_SUCCESS, "{0}: removed".format(name))
        removed += 1

    save_manifest(target_root, manifest)

    section("Summary")
    print("Removed:  {0}".format(removed))
    print("Skipped:  {0}".format(skipped))
    print("Failed:   {0}".format(failed))
    return 1 if failed else 0


# --------------------------------------------------------------------------- #
# Listing
# --------------------------------------------------------------------------- #


def run_list() -> int:
    profiles = discover_profiles()
    skills = discover_skills()

    section("Skills ({0})".format(len(skills)))
    for name, path in skills.items():
        skill_file = path / "SKILL.md"
        description = ""
        if skill_file.is_file():
            for line in skill_file.read_text(encoding="utf-8").splitlines()[:12]:
                if line.startswith("description:"):
                    description = line.split(":", 1)[1].strip()
                    break
        print("  {0}".format(name))
        if description:
            print("    {0}".format(description))

    section("Profiles ({0})".format(len(profiles)))
    for name, path in profiles.items():
        profile_name, description, profile_skills = read_profile(path)
        print("  {0}  (name: {1}, {2} skill(s))".format(name, profile_name, len(profile_skills)))
        if description:
            print("    {0}".format(description))
        for skill in profile_skills:
            mark = "" if skill in skills else "  (missing from skills/)"
            print("      - {0}{1}".format(skill, mark))
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="install.py",
        description="Install, verify, and uninstall the Agent Engineering Standards skills.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python scripts/install.py --list\n"
            "  python scripts/install.py --agent codex --profile full\n"
            "  python scripts/install.py --agent claude-code --profile full --scope user\n"
            "  python scripts/install.py --agent codex --skill production-logging\n"
            "  python scripts/install.py --agent codex --profile full --dry-run\n"
            "  python scripts/install.py --agent codex --profile full --uninstall\n"
        ),
    )
    parser.add_argument("--agent", choices=sorted(AGENTS), help="Target agent platform.")
    parser.add_argument(
        "--profile",
        help="Install all skills declared by a profile in profiles/.",
    )
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        metavar="NAME",
        help="Install a single skill by name. Repeatable.",
    )
    parser.add_argument(
        "--scope",
        choices=("project", "user"),
        default="project",
        help="Install into the current project (default) or the user home directory.",
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path.cwd(),
        help="Project root used for --scope project. Defaults to the current directory.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing skills and remove user-modified files during uninstall.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the plan without creating, modifying, or deleting any file.",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Remove skills that were installed by this tool.",
    )
    parser.add_argument("--list", action="store_true", help="List available skills and profiles.")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.list:
            return run_list()
        if not args.agent:
            raise InstallError(
                "--agent is required. Supported agents: {0}. Use --list to see the available options.".format(
                    ", ".join(sorted(AGENTS))
                )
            )
        profiles = discover_profiles()
        if args.profile and args.profile not in profiles:
            raise InstallError(
                "Unknown profile '{0}'. Available profiles: {1}.".format(
                    args.profile, ", ".join(sorted(profiles))
                )
            )
        if args.uninstall:
            return run_uninstall(
                args.agent,
                args.scope,
                args.project_dir.resolve(),
                args.profile,
                args.skill,
                args.force,
                args.dry_run,
            )
        return run_install(
            args.agent,
            args.scope,
            args.project_dir.resolve(),
            args.profile,
            args.skill,
            args.force,
            args.dry_run,
        )
    except InstallError as exc:
        emit(STATUS_FAILED, str(exc))
        return 1
    except KeyboardInterrupt:
        emit(STATUS_FAILED, "interrupted")
        return 130


if __name__ == "__main__":
    sys.exit(main())
