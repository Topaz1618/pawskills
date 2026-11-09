# Adapter: Claude Code

Installs the Agent Engineering Standards into a Claude Code workspace.

---

## What This Adapter Does

Claude Code reads skills from a `skills/` directory containing one Markdown file per skill, each with YAML frontmatter. This adapter places the repository's `skills/<name>/SKILL.md` files into that layout.

| Scope | Flag | Destination |
|---|---|---|
| Current project | `--scope project` (default) | `<project-dir>/.claude/skills/` |
| Current user | `--scope user` | `~/.claude/skills/` |

---

## Install

```bash
python3 scripts/install.py --agent claude-code --profile full
```

Common variations:

```bash
# A narrower baseline
python3 scripts/install.py --agent claude-code --profile development

# Individual standards
python3 scripts/install.py --agent claude-code --skill production-logging

# Preview without writing anything
python3 scripts/install.py --agent claude-code --profile full --dry-run

# Install into another project
python3 scripts/install.py --agent claude-code --profile full --project-dir /path/to/project
```

---

## Resulting Layout

```
.claude/skills/
├── task-execution-governance/
│   └── SKILL.md
├── production-logging/
│   └── SKILL.md
└── ...
└── .pawskills-manifest.json
```

The manifest is written by the installer and records the source path, installation time, and the SHA-256 hash of every installed file. It is what makes a later uninstall safe.

---

## Verification

The installer verifies after every install and reports the real result per skill:

```
[SUCCESS] production-logging: verified
```

Verification compares the installed file set and each file's hash against the source. A mismatch is reported as `[FAILED]`, not silently repaired.

To check the installation independently:

```bash
python3 scripts/install.py --agent claude-code --profile full --dry-run --project-dir .
```

A correctly installed skill shows no conflict. To confirm the content, open `.claude/skills/<name>/SKILL.md` and compare it with `skills/<name>/SKILL.md` in this repository.

---

## Overwrite and Uninstall Behaviour

- An existing skill directory is **never** overwritten by default. It is reported as `SKIPPED` and the remaining skills still install.
- `--force` backs the previous version up to `.pawskills-backups/<skill>-<timestamp>/` before replacing it.
- `--uninstall` removes only skills listed in the manifest. Skills you created yourself are left untouched.
- A file you edited after installation is reported and skipped during uninstall unless `--force` is given.

```bash
python3 scripts/install.py --agent claude-code --profile full --uninstall
```

---

## Manual Installation

If you prefer not to use the installer, copy the directories directly:

```bash
mkdir -p .claude/skills
cp -R skills/task-execution-governance .claude/skills/
cp -R skills/production-logging .claude/skills/
```

Two consequences of manual installation:

1. No manifest is written, so `--uninstall` will not remove these copies.
2. No hash is recorded, so the installer cannot detect that you have modified them.

The installer exists to avoid both problems. Use it unless there is a reason not to.

---

## Notes

- Skills are plain Markdown. Nothing in this repository requires a Claude Code extension or plugin.
- The `trigger` field in the frontmatter is a keyword list. It is advisory metadata for skill selection, not a hook.
- To apply standards to a single project only, install with `--scope project`. To apply them across all your projects, install with `--scope user`.

---

## Related Documents

- [Codex adapter](../codex/README.md) — the same standards for a different agent layout.
- [Generic agent adapter](../generic-agent/README.md) — how to use these standards without a specific agent.
- [Installation](../../README.md#installation) — the full installer reference.
- [Profiles](../../profiles/) — which standards each baseline includes.
