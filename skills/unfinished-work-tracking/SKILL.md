---
name: unfinished-work-tracking
description: Unfinished work tracking standard. Requires recording requirements, defects, omissions, and items pending verification that are discovered during development but not yet resolved.
trigger: TODO, unfinished, incomplete, 未完成, 遗漏, 没做, 部分完成, follow-up, remaining work
---

# Unfinished Work Tracking Standard

## I. Core Principle

Any relevant work discovered during execution but not actually completed must be recorded.

Unfinished information must not be discarded merely because the current task ended, the context switched, or the user did not ask about it.

## II. Situations That Require Recording

Include:

- An explicit requirement that has not been implemented.
- Only part of a feature was completed.
- A gap was discovered in existing functionality.
- A problem was discovered that needs fixing.
- An interface was discovered that needs adjustment.
- Documentation was discovered to be out of sync.
- A matter was discovered that needs further investigation.
- Something temporarily cannot be completed due to environment or dependency issues.
- Something believed to be implemented was found, upon inspection, to actually not be implemented.

## III. Situations That Do Not Require Recording

- Random thoughts unrelated to the current task.
- Problems that have actually been completed.
- Speculation with no clear action value.
- Duplicate items already recorded with no new information.

## IV. Record Format

By default, use the project's existing TODO file.

If the project has no unified recording location, use TODO.md.

Format:

- [ ] Outstanding item
  - Reason: why it needs to be handled.
  - Impact: which function it affects.
  - Related files: which files are involved.
  - Current status: why it is not completed.

For complex items, add necessary reproduction steps and verification conditions where needed.

Do not build an unnecessarily complex task management system.

## V. Check Before Execution

Before starting development:

1. Review the existing outstanding items.
2. Check whether the current task involves any of them.
3. Determine whether they can be completed along the way.
4. If they affect the correctness of the current task, resolve them first.

## VI. During Execution

When a new item is discovered:

- If it can be safely completed: complete it directly.
- If it requires additional work: record it.
- If it is temporarily impossible: record the reason.
- If an existing item has been resolved: update its status.
- If an old record turns out to be inaccurate: correct the record.

## VII. Check Before Delivery

Before delivery, confirm:

1. Are there outstanding items?
2. Are there features that are only half completed?
3. Are there tests that were not executed?
4. Is there documentation that is not in sync?
5. Are there problems that were discovered but not yet handled?
6. Have they all been recorded?

Partial completion must not be described as full completion.

## VIII. Completion Status

Only work that was actually completed may be marked as completed.

A test that did not pass must not be marked as passed.

An operation that was not executed must not be marked as executed.

Functionality that was not verified must not be marked as verified.

## IX. Final Principle

Not having told the user does not mean there are no outstanding items.

Unfinished work must have a record and must not disappear silently.
