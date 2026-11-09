# Adapter: Generic Agent

How to use the Agent Engineering Standards with an agent that has no dedicated skill directory.

---

## When to Use This Adapter

The `claude-code` and `codex` adapters install skills into a layout those agents read automatically. If your agent does not read such a directory, use this adapter.

The standards themselves are plain Markdown. They do not depend on any agent runtime.

Typical cases:

- An agent that loads instructions from a system prompt, a project instruction file, or a rules directory.
- An agent that reads documents from a knowledge base rather than a filesystem directory.
- A team that wants the standards in a repository as a documented reference, enforced through review rather than tooling.
- A custom or self-hosted agent with its own convention.

---

## The Standards Are Agent-Agnostic

Each standard under `skills/<name>/SKILL.md` consists of:

1. **YAML frontmatter** — `name`, `description`, `trigger`.
2. **A body of direct obligations** — what the agent must and must not do.

The body is written as instructions to the agent, in imperative form, with checkable requirements. It contains no agent-specific API calls, tool names, or runtime assumptions.

The frontmatter is metadata for skill selection. If your agent has no skill-loading mechanism, the frontmatter is simply the first block of the document and can be dropped.

---

## Method 1: Copy the Directory (simplest)

Place the skill folders where your agent expects to find instruction documents.

```bash
mkdir -p <your-agent's-instruction-dir>
cp -R skills/<name> <your-agent's-instruction-dir>/
```

Adapt `<your-agent's-instruction-dir>` to your agent's convention — a `.rules/` directory, an `instructions/` directory, or wherever it looks for behavioral instructions.

The installer does not support arbitrary directories, because it cannot know your agent's layout. The `claude-code` and `codex` adapters exist precisely because those layouts are known and fixed.

---

## Method 2: Reference from an Instruction File

Point your agent at the standards instead of copying them, so the repository stays the single source of truth.

```
Read and follow skills/task-execution-governance/SKILL.md before starting any implementation task.
Before writing any function, read skills/code-asset-inventory/SKILL.md and confirm the capability does not already exist.
Before reporting completion, read skills/testing-verification/SKILL.md and skills/change-report-delivery/SKILL.md.
```

This keeps a single copy of each standard and makes updates take effect immediately.

---

## Method 3: Generate a Consolidated Brief

When your agent accepts one instruction document rather than a set of files, concatenate the standards you have selected.

```bash
python3 - <<'PY'
from pathlib import Path

selected = ["task-execution-governance", "production-logging", "testing-verification"]
parts = []
for name in selected:
    text = Path("skills", name, "SKILL.md").read_text(encoding="utf-8")
    body = text.split("---", 2)[2].lstrip()  # drop frontmatter
    parts.append("# {0}\n\n{1}".format(name, body))
Path("AGENT_STANDARDS.md").write_text("\n\n---\n\n".join(parts) + "\n", encoding="utf-8")
print("wrote AGENT_STANDARDS.md")
PY
```

Keep the generated file out of version control, or regenerate it in CI, so it cannot drift from the sources. If you commit it, treat a mismatch between it and `skills/` as a validation failure.

---

## Method 4: Reference Repository Convention

If your agent reads a project-level instruction file — `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `CONVENTIONS.md` — point it at the standards from there.

```markdown
## Engineering standards

This project follows the Agent Engineering Standards in `skills/`.

- Task scoping and standard selection: `skills/task-execution-governance/SKILL.md`
- Reuse before writing new code: `skills/code-asset-inventory/SKILL.md`
- Verification and honest reporting: `skills/testing-verification/SKILL.md`, `skills/change-report-delivery/SKILL.md`
```

A pointer plus the selection rationale is more useful than pasting the full text, because it keeps the rules short enough to be followed.

---

## Selecting Which Standards Apply

Use a profile as the starting point, then adjust.

| Profile | Standards | Best for |
|---|---|---|
| [`full`](../../profiles/full.yaml) | All | A shared codebase with real downstream cost |
| [`development`](../../profiles/development.yaml) | 8 | Day-to-day feature work |
| [`data`](../../profiles/data.yaml) | 7 | Data pipelines, analysis, and research |
| [`lightweight`](../../profiles/lightweight.yaml) | 3 | Small or exploratory work |

Each profile has a README describing exactly what it enforces and what it omits.

---

## Verifying Adoption

A standard that is not followed is worse than no standard, because it creates a false expectation. Check adoption against the requirements themselves, not against whether the files are present.

The acceptance questions are already written down in each standard. For example, `data-audit-reproducibility` requires that a reviewer can answer:

- Where is the raw data?
- Where did the data come from?
- Is the raw data complete?
- What processing did each step undergo?
- Which records were excluded, and why?
- Which execution produced this result?

If those questions cannot be answered from the artifacts, the standard was not applied — regardless of whether the file was copied into the right directory.

---

## Notes

- The `trigger` field only makes sense if your agent supports keyword-based skill selection. Without that, select skills explicitly.
- The standards are written in English so that they behave identically across languages. Chinese trigger keywords in the frontmatter cover Chinese-language sessions.
- This repository's own standards apply to this repository. See [Engineering Principles](../../references/engineering-principles.md).

---

## Related Documents

- [Claude Code adapter](../claude-code/README.md) — automatic skill loading for Claude Code.
- [Codex adapter](../codex/README.md) — automatic skill loading for Codex.
- [Engineering Principles](../../references/engineering-principles.md) — why these standards exist.
- [Profiles](../../profiles/) — which standards each baseline includes.
