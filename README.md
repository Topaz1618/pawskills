# Agent Engineering Standards

A curated set of **14 engineering standards for AI coding agents**, distributed as portable Markdown skills.

Every standard is a self-contained instruction document. An agent that reads one knows exactly what is expected of it: how to scope a task, when to reuse existing code, what to log, how to verify, and how to report results honestly.

[简体中文](README.zh-CN.md)

---

## Why This Exists

AI coding agents fail in predictable ways. They re-run work that was already done, duplicate functions that already exist, ship interfaces nobody documented, produce logs that hide failures, claim tests passed without running them, and describe plans as completed work.

Each standard here targets one of those failure modes. Together they define what "done" means for an agent.

---

## The 14 Standards

| # | Skill | Core responsibility |
|---|---|---|
| 01 | `task-execution-governance` | Task identification, execution scope, standard coordination |
| 02 | `data-first-execution` | Prefer existing data; forbid unjustified re-runs |
| 03 | `code-asset-inventory` | Code asset inventory and function reuse |
| 04 | `interface-contract` | Interface contracts and unified data structures |
| 05 | `data-audit-reproducibility` | Raw data, data audit, reproducibility |
| 06 | `production-logging` | Raw logs, execution path, exception records |
| 07 | `testing-verification` | Testing, verification, independent review |
| 08 | `engineering-transparency` | Engineering transparency; file and function descriptions |
| 09 | `technical-documentation` | Authenticity and completeness of technical documentation |
| 10 | `documentation-structure` | Documentation organization and reading order |
| 11 | `language-expression` | Language expression and terminology |
| 12 | `change-report-delivery` | Change reports and delivery |
| 13 | `unfinished-work-tracking` | Tracking unfinished work |
| 14 | `explicit-instruction-fidelity` | Following explicit instructions without unauthorized reinterpretation |

---

## Repository Layout

```
agent-engineering-standards/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── SECURITY.md
│
├── skills/
│   ├── task-execution-governance/SKILL.md
│   ├── data-first-execution/SKILL.md
│   ├── code-asset-inventory/SKILL.md
│   ├── interface-contract/SKILL.md
│   ├── data-audit-reproducibility/SKILL.md
│   ├── production-logging/SKILL.md
│   ├── testing-verification/SKILL.md
│   ├── engineering-transparency/SKILL.md
│   ├── technical-documentation/SKILL.md
│   ├── documentation-structure/SKILL.md
│   ├── language-expression/SKILL.md
│   ├── change-report-delivery/SKILL.md
│   ├── unfinished-work-tracking/SKILL.md
│   └── explicit-instruction-fidelity/SKILL.md
│
├── profiles/
│   ├── full.yaml
│   ├── data.yaml
│   ├── development.yaml
│   ├── lightweight.yaml
│   ├── full-engineering/README.md
│   ├── data-engineering/README.md
│   ├── development/README.md
│   └── lightweight/README.md
│
├── adapters/
│   ├── claude-code/README.md
│   ├── codex/README.md
│   └── generic-agent/README.md
│
├── references/
│   ├── engineering-principles.md
│   ├── terminology.md
│   └── audit-data-model.md
│
├── scripts/
│   ├── install.py
│   ├── validate.py
│   └── check-links.py
│
└── tests/
    ├── test_skill_structure.py
    ├── test_frontmatter.py
    └── fixtures/
```

---

## Profiles

Not every team wants all 14 standards. A data team may need four; a solo developer may want two. Profiles are machine-readable YAML files that declare which skills a given working style requires.

| Profile | Skills | Intended for |
|---|---|---|
| [`full.yaml`](profiles/full.yaml) | All 14 | Teams enforcing a complete engineering baseline |
| [`data.yaml`](profiles/data.yaml) | 8 | Data engineering, analytics, and research work |
| [`development.yaml`](profiles/development.yaml) | 9 | Day-to-day feature development |
| [`lightweight.yaml`](profiles/lightweight.yaml) | 4 | Minimal guardrails for small or exploratory work |

Each profile directory contains a README explaining when to choose it and what it enforces.

---

## Installation

```bash
git clone <repository-url>
cd pawskills
python3 scripts/install.py --agent codex --profile full
```

That is the whole setup. The installer copies the skill directories into the target agent's skills folder and records what it installed so it can be removed later.

### Supported Agents

| Agent | Project scope | User scope |
|---|---|---|
| `claude-code` | `.claude/skills/` | `~/.claude/skills/` |
| `codex` | `.agents/skills/` | `~/.agents/skills/` |

### Installation Scope

| Scope | Flag | Destination |
|---|---|---|
| Current project | `--scope project` (default) | `<project-dir>/.agents/skills/` or `<project-dir>/.claude/skills/` |
| Current user | `--scope user` | `~/.agents/skills/` or `~/.claude/skills/` |

Use `--project-dir /path/to/project` to install into a project other than the current directory.

### Install a Profile

A profile is a named set of skills declared in `profiles/*.yaml`.

```bash
python3 scripts/install.py --agent codex --profile full
python3 scripts/install.py --agent claude-code --profile data
python3 scripts/install.py --agent codex --profile development
python3 scripts/install.py --agent codex --profile lightweight
```

### Install Individual Skills

```bash
python3 scripts/install.py --agent codex --skill production-logging
python3 scripts/install.py --agent codex --skill production-logging --skill testing-verification
```

`--skill` is repeatable and can be combined with `--profile`.

### List What Is Available

```bash
python3 scripts/install.py --list
```

Prints every skill with its description and every profile with the skills it contains.

### Overwrite Protection

Existing skills are never overwritten by default. A conflicting skill is reported as `SKIPPED` and the remaining skills still install.

```bash
python3 scripts/install.py --agent codex --profile full --force
```

With `--force`, the previous version is copied to `.pawskills-backups/` before it is replaced.

### Preview

```bash
python3 scripts/install.py --agent codex --profile full --dry-run
```

Prints the source path, target path, conflict status, and the files that would be overwritten. No file is created, modified, or deleted.

### Uninstall

```bash
python3 scripts/install.py --agent codex --profile full --uninstall
python3 scripts/install.py --agent codex --skill production-logging --uninstall
```

Only skills recorded in the Pawskills manifest are removed. Skills the user created themselves are left alone, and files the user modified after installation are reported and skipped unless `--force` is given.

### Common Errors

| Message | Cause | Fix |
|---|---|---|
| `--agent is required` | No agent was given | Add `--agent claude-code` or `--agent codex` |
| `Unknown profile '...'` | The profile name does not exist | Run `--list` to see the available profiles |
| `Skill '...' does not exist` | The skill name is not a directory under `skills/` | Run `--list` to see the available skills |
| `skipped, target already exists` | The skill is already installed | Use `--force` to overwrite |
| `modified after installation` | The files were changed after install | Use `--force` to remove them anyway |

---

## Skill Format

Each skill is one Markdown file with YAML frontmatter:

```yaml
---
name: production-logging
description: Production logging standard. Requires recording real execution facts...
trigger: log, logging, logger, 日志, 排错, trace, audit
---
```

- `name` — unique skill identifier.
- `description` — what the standard requires and when it applies.
- `trigger` — keywords that should cause an agent to load the skill.

The body contains the standard itself, written as direct instructions to the agent rather than as prose about the standard.

---

## Validation

```bash
python3 scripts/validate.py          # Validate skill structure, frontmatter, and profiles
python3 scripts/check-links.py        # Check internal links
python3 -m pytest tests/ -v           # Run the test suite
```

The test suite runs entirely against temporary directories and never modifies a real project.

---

## Reference Documents

These are not standards — the agent is not required to load them. They explain the reasoning and the vocabulary behind the standards.

| Document | Contents |
|---|---|
| [Engineering Principles](references/engineering-principles.md) | The ten principles every standard enforces, and how they map to the skills |
| [Terminology](references/terminology.md) | The controlled vocabulary, and the terms the repository deliberately avoids |
| [Audit Data Model](references/audit-data-model.md) | The concrete record structures behind `data-audit-reproducibility` |

## Agent Adapters

| Adapter | Covers |
|---|---|
| [Claude Code](adapters/claude-code/README.md) | Installation and verification for the `.claude/skills/` layout |
| [Codex](adapters/codex/README.md) | Installation and verification for the `.agents/skills/` layout |
| [Generic Agent](adapters/generic-agent/README.md) | Using these standards with an agent that has no skills directory |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New standards must follow the same structure, be self-contained, and address a specific failure mode rather than restating existing guidance.

---

## License

Released under the MIT License. See [LICENSE](LICENSE).
