---
name: repository-publication-hygiene
description: Repository publication hygiene standard. Requires agents to keep private references, tool attribution, and internal artifacts out of version-controlled content before a repository is published, and to keep every published configuration value explicit rather than implicitly leaked.
trigger: commit, push, publish, public repository, open source, git history, co-authored-by, trailer, attribution, README, credential, secret, private reference, gitignore, 开源, 提交, 推送, 发布, 私有信息, 署名, 凭据
---

# Repository Publication Hygiene Standard

## 1. Core Principle

**A published repository is a public document. Anything in it — including
commit metadata — is read by strangers, permanently, and cannot be recalled.**

The agent must assume any content that reaches a public remote is public
forever, including metadata that the agent did not deliberately write.

The standard for publication is not "the code works" but "nothing in this
repository identifies a person, an organization, an internal system, or the
tool that produced it, unless the owner explicitly asked for that."

## 2. Scope of Publication Hygiene

The agent must apply this standard to every artifact that leaves the local
working tree:

- Source files.
- README and documentation.
- Configuration templates and example files.
- Directory and file names.
- Git commit messages, author fields, and trailers.
- Branch names, tag names, and remote URLs.
- Commit history, including history rewritten with `rebase` or `amend`.

A leak in any one of these is a leak.

## 3. Private Reference Exclusion

The agent must not commit content that references internal systems,
organizations, sibling projects, private infrastructure, or the owner's local
environment, unless the owner explicitly requires it.

| Category | Examples of what to exclude |
|---|---|
| Sibling projects | Names of private or internal repositories |
| Internal infrastructure | Internal hostnames, subdomains, cluster names, bucket names |
| Local paths | Absolute paths containing the owner's home directory or user name |
| Internal accounts | Team account names, organization identifiers, internal org IDs |
| Unrelated credentials | Secrets for services this project never calls |

### 3.1 Detection

Before publishing, the agent must inspect the content that will be published
and search for:

- Absolute paths rooted at a home directory.
- The owner's user name or home directory name.
- Names of other projects on the same machine.
- Hostnames and domains that are not part of this project's public surface.
- Tokens, keys, and long opaque strings that resemble credentials.

The agent must also search the **commit history**, not only the working tree.
A file deleted in a later commit is still in the history.

### 3.2 Boundary Cases

A public name that happens to be similar to a private one is not a leak. The
question is whether the reference carries information about systems the owner
does not intend to disclose.

Documentation that names a public service the project genuinely calls is not a
leak. The requirement is to keep the *repository's own* public surface
accurate, not to strip every proper noun.

## 4. Tool Attribution Exclusion

**The agent must not add its own name, product name, account, or email address
to any published artifact.**

This includes, without limitation:

- `Co-authored-by` trailers.
- `Signed-off-by` trailers.
- `Generated with`, `Created by`, or similar message footers.
- File headers inserted automatically.
- Commit body lines naming the tool or the agent.
- Code comments attributing authorship to the tool.
- Directory or file names containing the tool name.

### 4.1 Why This Is a Hard Rule

Tool-integration layers often append attribution trailers automatically. The
agent must therefore treat the commit message as **output it must inspect**,
not merely a message it wrote.

A trailer the agent never typed is still the agent's responsibility, because
the agent ran the command that produced it.

### 4.2 Required Practice

After any commit that an integration may have augmented:

1. Read the commit message back (`git log -1 --format=%B`).
2. Check it for attribution trailers or tool names.
3. If one is present, remove it and rewrite the commit.

The agent must repeat this check after any history rewrite — `rebase`,
`amend`, or `filter-branch` — because these operations can re-introduce or
duplicate trailers.

### 4.3 Suppression

When the integration's automatic attribution cannot be turned off, the agent
must strip it explicitly rather than leaving it in place. This is a required
correction step, not an optional one.

A `prepare-commit-msg` git hook performs this suppression automatically before
the commit object is created. The hook in `scripts/hooks/prepare-commit-msg`
removes tool-attribution trailers while preserving trailers that name real
people. It can be installed for all repositories with:

```bash
mkdir -p ~/.cursor/hooks
cp scripts/hooks/prepare-commit-msg ~/.cursor/hooks/
chmod +x ~/.cursor/hooks/prepare-commit-msg
git config --global core.hooksPath ~/.cursor/hooks
```

A hook is a convenience, not a substitute for reading the commit message back.
The agent must still verify the result.

## 5. Configuration Transparency

**Every configuration value a user is expected to change must be present in
the example configuration file, and every value in that file must be visible
to the user as a placeholder or a documented default.**

- The example file must not contain real credentials. Secret fields are
  empty.
- Non-secret fields that the user must set are also empty, with a comment
  explaining what happens if they are left empty.
- A value that differs between deployments — a port, a host, a region, a
  bucket — belongs in the configuration file, not hardcoded in the source or
  in the documentation.

### 5.1 Empty Versus Filled

A placeholder file ships with **empty values**. Filling in a real port, host,
or address in the example file leaks the owner's deployment, and a README
that repeats it publishes it.

### 5.2 Default Handling

When a configuration value is empty, the code must fall back to a built-in
default. An empty configuration value must never overwrite a default with an
empty string; a missing value and an empty value are different states.

The consequence of this rule is that defaults live in code, where they are
visible to anyone reading the source, and the published configuration file
stays free of deployment specifics.

## 6. Pre-Publication Verification

Before the first push to a public remote, and before any push that publishes
new content, the agent must:

1. Confirm which files are tracked (`git ls-files`).
2. Confirm the ignore rules cover every artifact that must not ship:
   credentials, downloaded binaries, runtime manifests, personal notes, local
   state, logs, and generated output.
3. Scan the tracked files for private references and tool attribution.
4. Scan the commit history for the same.
5. Verify the example configuration file contains no real values.
6. Confirm the remote is the intended public remote.

A file that is present in the working tree but untracked is safe. A file that
is tracked is public.

## 7. Removing Something Already Published

Publishing is not reversible, but a leak in the **current** history is
correctable. When the agent discovers that unwanted content was published:

1. Report the scope precisely — which files, which commits.
2. Remove the content from the working tree.
3. Rewrite the affected history.
4. Force-push, using `--force-with-lease` rather than `--force`.
5. Verify the remote now matches the local history.

Do not report the correction as complete until the remote has been checked.

If the content also exists in forks, caches, or archives, state plainly that
the removal is incomplete and what remains exposed. Do not describe a
partial remediation as a full one.

## 8. The Owner's Author Identity

The commit author and committer identity belong to the owner. The agent must
not set, change, or guess it, and must not introduce a second identity
without explicit authorization.

When rewriting history, the agent must preserve the original author and
author date unless the owner asks otherwise.

## 9. Reporting

The agent must report, before and after publishing:

- The remote URL and the branch that will be pushed.
- The number and identity of the files in the push.
- The result of the private-reference scan, stated plainly.
- Any file that was excluded and how.
- Any history that was rewritten, and the old and new commit identifiers.

The agent must not describe a repository as clean because the code compiles.
The scan result is the evidence, and the evidence must be shown.

## 10. Relationship to Other Standards

- Whether an operation was authorized at all is governed by
  `user-intent-priority`.
- Whether the requested operation was performed literally is governed by
  `explicit-instruction-fidelity`.
- Whether the verification steps actually ran, and what they found, is
  governed by `testing-verification`.
- How the final state is reported is governed by `change-report-delivery`.

## 11. Highest Priority Rule

**Everything that reaches a public remote is public, permanent, and read by
strangers. The agent owns every byte of it, including the bytes it did not
write on purpose.**
