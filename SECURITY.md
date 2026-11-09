# Security Policy

## Reporting a Vulnerability

Please report suspected vulnerabilities privately rather than through a public issue.

- Use the repository's private vulnerability reporting form if one is enabled.
- Otherwise, open a security advisory on the repository, or contact the maintainers directly.
- Include the affected file or version, a description of the issue, and reproduction steps.

Do not open a public issue for an unfixed vulnerability.

You can expect an acknowledgement within a few days. Fix timing depends on severity; the reporter is kept informed of progress.

---

## What This Project Is

This repository contains Markdown documents — engineering standards for AI coding agents — plus a small set of Python scripts that install and validate them.

**The repository contains no application, no server, no network service, and no authentication layer.** The threat model is therefore narrow, and it is worth stating precisely rather than leaving it implied.

---

## Threat Model

### What the scripts do

`scripts/install.py`, `scripts/validate.py`, and `scripts/check-links.py`:

- Read files from this repository and from the directory they are invoked in.
- Write files into a target skills directory under the current project or the user's home directory.
- Write a manifest file (`.pawskills-manifest.json`) and, with `--force`, a backup directory (`.pawskills-backups/`).
- Make no network requests.

### What the scripts do not do

They never:

- Read or transmit credentials, tokens, SSH keys, or environment secrets.
- Access anything outside the repository and the explicitly selected target directory.
- Execute installed skill content. A skill is Markdown; it is read by an agent, not run by the installer.
- Modify the source skills under `skills/`.
- Install third-party packages or dependencies.

The only dependency is PyYAML, and it is optional — the scripts fall back to a built-in parser for the YAML subset these files use.

---

## Known Limitations

These are properties of the current design, stated so they are not mistaken for guarantees.

| Limitation | Impact | Mitigation |
|---|---|---|
| A skill directory that already exists is not overwritten unless `--force` is passed | The installer will not silently replace your work | Overwrite protection is the default; `--force` backs up first |
| `--force` deletes the previous skill directory after copying it to `.pawskills-backups/` | A failed copy could leave the target incomplete | The copy is performed before the removal and the backup path is reported |
| Uninstall compares SHA-256 hashes to decide whether a file was modified | A file edited to the same content is not distinguished from an unmodified one | The consequence is limited: the file is left in place rather than deleted |
| Skill content is Markdown that an agent may read and follow | A malicious skill could instruct an agent to act against the user's intent | Skills are reviewed before merging; see below |
| The manifest records absolute source paths | The manifest discloses the local filesystem layout | The manifest stays inside the target skills directory |

---

## Trusting Installed Skills

Installing a skill means placing a document into a directory your agent reads. A skill is an instruction to an agent, and an agent with file or command access may act on it.

Therefore:

- **Review skills before installing them.** This repository's skills are in `skills/` and are readable in full before any install.
- **Treat third-party skills as code.** The same review that applies to a dependency applies to a skill.
- **Prefer a pinned version.** Install from a tag or a reviewed commit rather than an unreviewed branch.
- **Keep the overwrite protection on.** Do not pass `--force` against a target directory whose contents you have not inspected.

Uninstalling removes only what the manifest records, so a skill you did not install through this tool is never removed by it.

---

## Handling Sensitive Data

The standards in this repository describe how an agent should handle data. Two rules apply to this repository itself:

1. **Do not commit secrets.** No credentials, tokens, private keys, or `.env` files belong in this repository. `.gitignore` excludes common local artifacts.
2. **Do not commit customer data as examples.** Examples in the standards use placeholder values.

If a secret is accidentally committed, treat it as compromised: rotate it, then remove it from the history. Rewriting history does not un-publish the value.

---

## Reporting Scope

In scope:

- A script that writes outside its declared target directory.
- A script that executes content it should not execute.
- A path-handling flaw that allows a crafted skill name or profile to write to an unintended location.
- An install or uninstall flow that deletes a file it did not install, without `--force`.

Out of scope:

- The content of a standard being unsound as engineering guidance. That is a documentation issue; open a normal issue.
- Vulnerabilities in an agent platform that reads these skills. Report those to the agent's maintainer.
- Reports without a reproducible description. Ask for clarification and keep the issue open.

---

## Supported Versions

| Version | Supported |
|---|---|
| 0.1.x | Yes |
| < 0.1.0 | No |

Fixes are applied to the latest release. There is no long-term support branch at this time.

---

## Security-Relevant Contributions

Changes to `scripts/` are reviewed with extra attention. A pull request touching the installer should state:

- Which files it reads and which it writes.
- Whether it expands the set of paths the installer can touch.
- Whether the change affects the overwrite protection or the uninstall safety checks.

New behaviour that widens the installer's reach needs to be justified in the pull request description, not only in the code.

---

## Related Documents

- [Contributing](CONTRIBUTING.md) — how to propose a change.
- [Code of Conduct](CODE_OF_CONDUCT.md) — expected behaviour in project spaces.
- [Changelog](CHANGELOG.md) — what changed in each release.
