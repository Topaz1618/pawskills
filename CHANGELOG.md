# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- `references/engineering-principles.md` — The ten principles underlying every standard, and how they map to the skills.
- `references/terminology.md` — The controlled vocabulary, including the terms the repository deliberately avoids.
- `references/audit-data-model.md` — Concrete record structures (source, transformation, reconciliation, execution, modification, privacy) behind `data-audit-reproducibility`.
- `adapters/claude-code/README.md` — Installation and verification guide for the Claude Code layout.
- `adapters/codex/README.md` — Installation and verification guide for the Codex layout.
- `adapters/generic-agent/README.md` — Four methods for using these standards with an agent that has no dedicated skills directory.
- `SECURITY.md` — Reporting process, threat model, known limitations, and supported versions.

### Changed

- All four profiles now include `explicit-instruction-fidelity`. The standard was previously shipped but not installable through any profile.
- `profiles/*.yaml` skill counts and the profile READMEs updated to match: full 14, development 9, data 8, lightweight 4.
- `README.md` and `README.zh-CN.md` list all 14 standards; the standards table and repository layout were updated accordingly.
- `task-execution-governance` now references skills by their directory names. The previous references to `engineering-transparency-standard`, `data-audit-reproducibility-standard`, and `production-logging-standard` did not resolve to any skill.

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
