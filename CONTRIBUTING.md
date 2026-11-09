# Contributing

Thank you for considering a contribution. This document explains how to propose changes, what a new standard must look like, and how the repository is validated.

---

## Getting Started

```bash
git clone <repository-url>
cd pawskills
python3 -m pip install pytest
python3 scripts/validate.py
python3 -m pytest tests/ -v
```

All checks must pass before a pull request is opened.

---

## Contribution Types

### 1. Fixing a Standard

Correcting a rule that is ambiguous, wrong, or contradicted by another standard. Include the exact section and what was wrong.

### 2. Adding a Standard

A new standard that addresses a distinct failure mode not already covered. See [Writing a Standard](#writing-a-standard).

### 3. Adding or Revising a Profile

A profile is a named subset of the standards for a particular working style. New profiles must state who they are for and what they enforce.

### 4. Improving the Tooling

The installer, the validator, the link checker, or the test suite.

### 5. Improving the Documentation

The READMEs, the profile guides, the adapter guides, and the reference documents.

---

## Writing a Standard

Every standard lives in `skills/<skill-name>/SKILL.md` and follows a fixed format.

### Directory and file layout

```
skills/<skill-name>/SKILL.md
```

The directory name and the `name` field in the frontmatter must be identical. The validator rejects any mismatch.

### Frontmatter

```yaml
---
name: production-logging
description: Production logging standard. Requires recording real execution facts, raw requests and responses, exceptions, data changes, and the complete execution path.
trigger: log, logging, logger, 日志, 排错, trace, audit
---
```

- `name` must be slug style: lowercase letters, digits, and single hyphens.
- `description` states what the standard requires and when it applies. Write it in the third person, starting with the subject.
- `trigger` lists the keywords that should cause an agent to load the skill. Include both English and Chinese terms when the standard is likely to be invoked in a Chinese-language session.

### Body

The body is written as **direct instructions to the agent**, not as prose describing the standard. Read an existing standard before writing a new one; the house style is:

1. A numbered core principle that states the rule in one or two sentences.
2. Numbered sections that expand the rule into concrete, checkable obligations.
3. Use tables for decision matrices and for lists of required fields.
4. Use imperative wording: "Must", "Forbidden", "Must be able to answer".
5. State what a failure looks like, so the agent can recognise it.

### Requirements for a new standard

- It must address a **specific failure mode** that an agent actually exhibits. "Better code quality" is not a failure mode; "claims a test passed without running it" is.
- It must be **self-contained**. A reader should not need another standard to understand it, though it may point to related standards by name.
- It must not **restate** an existing standard. If two standards would say the same thing, merge them.
- It must be **actionable**. Every obligation must be checkable by a reviewer.
- It must not contain **project-specific** paths, table names, or business rules. These standards apply to any repository.
- It must be written in **English**, since the standards are read by agents regardless of the user's language. Chinese trigger keywords are welcome in the frontmatter.

### Length

There is no fixed limit. A standard should be as long as its rules require and no longer. Prefer a table over a repeated paragraph, and delete any section that repeats another.

---

## Editing an Existing Standard

- Keep the same heading structure. The validator does not enforce it, but consistent structure makes the set readable as a whole.
- Update the `description` and `trigger` fields if the scope of the standard changed.
- If you rename a skill directory, update every reference to it in `skills/`, `profiles/`, and the READMEs. Run `python3 scripts/check-links.py` afterwards.
- If a standard gains or loses a dependency on another standard, update the table in `task-execution-governance`.

---

## Editing a Profile

```yaml
name: data-engineering
description: Data auditing, processing and reproducibility standards.

skills:
  - task-execution-governance
  - data-first-execution
```

- The `skills` list must only contain directories that exist under `skills/`. The validator checks this.
- Every profile must have a non-empty `name` and `description`.
- Do not hardcode skill lists anywhere in `scripts/`. The profile files are the single source of truth.

---

## Pull Request Checklist

- [ ] `python3 scripts/validate.py` passes.
- [ ] `python3 scripts/check-links.py` passes.
- [ ] `python3 -m pytest tests/ -v` passes.
- [ ] New skills follow the format above and their directory name matches the frontmatter `name`.
- [ ] New profiles list only existing skills.
- [ ] `CHANGELOG.md` has an entry under `[Unreleased]`.
- [ ] README tables updated if skills or profiles were added or renamed.

---

## Commit Messages

Use a short imperative summary, one line, in the present tense.

```
Add interface contract standard
Fix uninstall protection for user-modified files
Update full profile with the new standard
```

---

## Reporting Problems

Open an issue describing what an agent did, which standard should have prevented it, and what the standard currently says. Concrete examples are far more useful than general descriptions.

---

## License

Contributions are accepted under the MIT License. See [LICENSE](LICENSE).
