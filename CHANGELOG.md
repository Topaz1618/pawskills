# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- `skills/engineering-context-completeness/SKILL.md` — Engineering context and logical completeness. Requires the problem to be understood before a solution is proposed; requires a complete chain of technical logic before concrete implementation is discussed; requires strict separation of current state, problem, recommendation, and item pending confirmation; requires a complete causal chain from every recommendation to its cost and risk, including the recommendation to keep the existing implementation when it already satisfies the requirement; forbids unauthorized expansion of the change scope; requires cross-turn continuity of verified facts and user decisions; requires a complete conclusion rather than repeated confirmation requests; and requires a full implementation plan before any code or database change.
- `.cursor/rules/engineering-context.mdc` — The same constraints as a Cursor project rule with `alwaysApply: true`, so they apply on every prompt in this repository rather than only when a skill is triggered.
- `references/engineering-principles.md` — The eleven principles underlying every standard, and how they map to the skills.
- `references/terminology.md` — The controlled vocabulary, including the terms the repository deliberately avoids.
- `references/audit-data-model.md` — Concrete record structures (source, transformation, reconciliation, execution, modification, privacy) behind `data-audit-reproducibility`.
- `adapters/claude-code/README.md` — Installation and verification guide for the Claude Code layout.
- `adapters/codex/README.md` — Installation and verification guide for the Codex layout.
- `adapters/generic-agent/README.md` — Four methods for using these standards with an agent that has no dedicated skills directory.
- `SECURITY.md` — Reporting process, threat model, known limitations, and supported versions.
- `skills/user-intent-priority/SKILL.md` — User intent recognition and response priority. Classifies every user message as a question, a discussion, an execution instruction, or a mix; requires answering before executing; requires an autonomous task to pause when the user speaks; and gates every tool call on actual authorization.
- `skills/repository-publication-hygiene/SKILL.md` — Repository publication hygiene. Defines what may and may not reach a public remote: excludes private references, sibling project names, local paths, and unrelated credentials; forbids the agent from adding its own name to any published artifact, including `Co-authored-by` trailers added automatically by an integration; requires the commit message to be read back and cleaned after every commit; requires example configuration files to ship with empty values and the code to fall back to built-in defaults; and requires a pre-publication scan of both the tracked files and the commit history.

### Changed

- All four profiles now include `engineering-context-completeness`, so the context and completeness constraints cannot be opted out of.
- All four profiles now include `repository-publication-hygiene`, so it cannot be opted out of.

- All four profiles now include `explicit-instruction-fidelity`. The standard was previously shipped but not installable through any profile.
- All four profiles now include `user-intent-priority`.
- `profiles/*.yaml` skill counts and the profile READMEs updated to match: full 17, development 12, data 11, lightweight 7.
- `README.md` and `README.zh-CN.md` list all 17 standards; the standards table and repository layout were updated accordingly.
- `task-execution-governance` now references skills by their directory names. The previous references to `engineering-transparency-standard`, `data-audit-reproducibility-standard`, and `production-logging-standard` did not resolve to any skill.
- `task-execution-governance` section IX was reduced to a pointer to `user-intent-priority`, and `user-intent-priority` was added to its task type table and standard priority list.
- `technical-documentation` sections IX and X add the natural-language and terminology rules, and the required organization of a functional module document.
- `language-expression` section VIII forbids colloquial expression and non-standard terminology across all forms of output.
- `language-expression` section IX forbids arbitrary abbreviation and compressed code naming. It covers variable names, function and class names, JSON, YAML, and configuration keys, database column names, file and directory names, data structure fields, API parameter names, and branch names; requires a complete expression for a quantity such as `page_count` rather than `n_pages`; forbids opaque single-letter prefixes such as `n_`, `cnt_`, `tmp_`, and `cfg_`; forbids forcing fields of different meanings into similar names for the sake of consistency; requires a new data structure to be understandable from its field names alone; and states that the priority is semantic clarity rather than a smaller character count or faster typing.
- `interface-contract` section 8.1 states that an existing field name must not be renamed on the agent's own initiative, and requires the impact on callers, historical data, migration, and compatibility to be analyzed and a proposal put forward first.
- `references/terminology.md` defines name, and lists the opaque prefixes the repository does not use.
- `references/terminology.md` and `references/engineering-principles.md` cover the new standard and the principle that user intent precedes the agent's plan.
- `references/terminology.md` now defines current state, problem, recommendation, to be confirmed, and implementation plan, and `references/engineering-principles.md` maps the new standard to the principle that reasoning is complete before action.

- `tests/test_skill_structure.py` — The expected skill set now includes `engineering-context-completeness`.

### Fixed

- The profile READMEs documented `--target claude-code`, which is not an installer option. They now use the real `--agent claude-code --profile <name>` form.
- The `Skill Format` example in both READMEs showed `name: production-logging-standard`. The frontmatter `name` must equal the directory name, which is `production-logging`.

---

## [0.1.0] - 2026-11-09

Initial release.

### Added

**Standards (14 skills)**

- `task-execution-governance` — Task identification, execution scope, standard coordination.
- `data-first-execution` — Prefer existing data; forbid unjustified re-collection and recomputation.
- `code-asset-inventory` — Code asset inventory and functional reuse.
- `interface-contract` — Interface contracts and unified data structures.
- `data-audit-reproducibility` — Raw data preservation, data audit, reproducibility.
- `production-logging` — Raw logs, execution path, exception records.
- `testing-verification` — Testing, verification, independent review.
- `engineering-transparency` — Engineering transparency, file and function descriptions.
- `technical-documentation` — Authenticity and completeness of technical documentation.
- `documentation-structure` — Documentation organization and reading order.
- `language-expression` — Language expression and terminology.
- `change-report-delivery` — Change reports and delivery.
- `unfinished-work-tracking` — Tracking unfinished work.
- `explicit-instruction-fidelity` — Follow explicitly specified operations without unauthorized reinterpretation.

**Profiles**

- `profiles/full.yaml` — All standards.
- `profiles/development.yaml` — Standards for day-to-day feature development.
- `profiles/data.yaml` — Standards for data engineering and analysis.
- `profiles/lightweight.yaml` — Minimum guardrails for small work.

**Tooling**

- `scripts/install.py` — Install, preview, verify, and uninstall skills for Claude Code and Codex.
- `scripts/validate.py` — Validate skill structure, frontmatter, and profile definitions.
- `scripts/check-links.py` — Check that relative Markdown links resolve.

**Tests**

- `tests/test_install.py` — Installer behaviour, including conflict handling and uninstall protection.
- `tests/test_skill_structure.py` — Skill directory and profile structure.
- `tests/test_frontmatter.py` — Frontmatter format, required keys, and name uniqueness.

**Continuous integration**

- `.github/workflows/validate.yml` — Runs validation, link checking, the test suite, and an installer smoke test on every push and pull request.

[Unreleased]: https://github.com/<owner>/<repository>/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/<owner>/<repository>/releases/tag/v0.1.0
