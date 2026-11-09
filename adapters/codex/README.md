# Adapter: Codex

Installs the Agent Engineering Standards into a Codex workspace.

---

## What This Adapter Does

Codex reads skills from a `skills/` directory containing one Markdown file per skill, each with YAML frontmatter. This adapter places the repository's `skills/<name>/SKILL.md` files into that layout.

| Scope | Flag | Destination |
|---|---|---|
| Current project | `--scope project` (default) | `<project-dir>/.agents/skills/` |
| Current user | `--scope user` | `~/.agents/skills/` |

Note the directory name: Codex uses `.agents/skills/`, while Claude Code uses `.claude/skills/`. The same standard files are installed into both, byte for byte.

---

## Install

```bash
python3 scripts/install.py --agent codex --profile full
```

Common variations:

```bash
# A narrower baseline
python3 scripts/install.py --agent codex --profile data

# Individual standards
python3 scripts/install.py --agent codex --skill production-logging
python3 scripts/install.py --agent codex --skill production-logging --skill testing-verification

# Preview without writing anything
python3 scripts/install.py --agent codex --profile full --dry-run

# Install into another project
python3 scripts/install.py --agent codex --profile full --project-dir /path/to/project
```

---

## Resulting Layout

```
.agents/skills/
├── task-execution-governance/
│   └── SKILL.md
├── data-first-execution/
│   └── SKILL.md
└── ...
└── .pawskills-manifest.json
```

The manifest is written by the installer and records the source path, installation time, and the SHA-256 hash of every installed file. It is what makes a later uninstall safe.

---

## Verification

The installer verifies after every install and reports the real result per skill:

```
[SUCCESS] data-first-execution: verified
```

Verification compares the installed file set and each file's hash against the source. A mismatch is reported as `[FAILED]`, not silently repaired.

To check the installation independently:

```bash
python3 scripts/install.py --agent codex --profile full --dry-run --project-dir .
```

A correctly installed skill shows no conflict. To confirm the content, open `.agents/skills/<name>/SKILL.md` and compare it with `skills/<name>/SKILL.md` in this repository.

---

## Overwrite and Uninstall Behaviour

- An existing skill directory is **never** overwritten by default. It is reported as `SKIPPED` and the remaining skills still install.
- `--force` backs the previous version up to `.pawskills-backups/<skill>-<timestamp>/` before replacing it.
- `--uninstall` removes only skills listed in the manifest. Skills you created yourself are left untouched.
- A file you edited after installation is reported and skipped during uninstall unless `--force` is given.

```bash
python3 scripts/install.py --agent codex --profile full --uninstall
```

---

## Manual Installation

If you prefer not to use the installer, copy the directories directly:

```bash
mkdir -p .agents/skills
cp -R skills/task-execution-governance .agents/skills/
cp -R skills/data-first-execution .agents/skills/
```

Two consequences of manual installation:

1. No manifest is written, so `--uninstall` will not remove these copies.
2. No hash is recorded, so the installer cannot detect that you have modified them.

The installer exists to avoid both problems. Use it unless there is a reason not to.

---

## Notes

- Skills are plain Markdown. Nothing in this repository requires a Codex extension or plugin.
- The `trigger` field in the frontmatter is a keyword list. It is advisory metadata for skill selection, not a hook.
- Installing into `.agents/skills/` at the user level makes the standards available in every project under `~/.agents/skills/`.
- The installer writes nothing outside the target skills directory and the manifest. It never modifies your source files.

---

## Related Documents

- [Claude Code adapter](../claude-code/README.md) — the same standards for a different agent layout.
- [Generic agent adapter](../generic-agent/README.md) — how to use these standards without a specific agent.
- [Installation](../../README.md#installation) — the full installer reference.
- [Profiles](../../profiles/) — which standards each baseline includes.
