---
name: change-report-delivery
description: Development change report and delivery standard. Requires truthfully describing added, modified, and deleted files, functions, logic, interfaces, and verification results.
trigger: 交付, 变更记录, 改了什么, 完成报告, 总结改动, delivery, changelog, change report
---

# Development Change Report and Delivery Standard

## I. Core Principle

After every development, modification, refactoring, fix, or configuration adjustment is complete, a delivery description consistent with the actual changes must be provided.

The user should not have to re-read all the source code in order to know what was done this time.

The following statements must not be used on their own as a delivery report:

- Development completed.
- Logic optimized.
- Issue fixed.
- Files updated.
- Testing completed.

## II. Overview of This Work

State:

1. The original objective.
2. The problem solved.
3. The work actually completed.
4. The final effect.
5. The content that is not yet complete.

Only report changes that actually occurred.

## III. File Change List

Divided into three categories.

### 1. Added Files

State:
- Complete path.
- File type.
- File purpose.
- Main responsibilities.
- Inputs and outputs.
- Related modules.

### 2. Modified Files

State:
- Complete path.
- Original responsibilities.
- Reason for the modification.
- Specific modification content.
- Responsibilities after the modification.
- Impact on other modules.

### 3. Deleted Files

State:
- Complete path.
- Original responsibilities.
- Reason for deletion.
- Whether functionality was migrated.
- Whether callers exist.
- Whether other modules are affected.

## IV. Function-Level Changes

### Added Functions

State:
- Function name.
- Containing file.
- Functionality.
- Input parameters.
- Return value.
- Core logic.
- Call relationships.

### Modified Functions

State:
- Function name.
- Behavior before the modification.
- Reason for the modification.
- Specific logic changes.
- Behavior after the modification.
- Whether inputs and outputs changed.
- Impact on callers.

### Deleted Functions

State:
- Function name.
- Original functionality.
- Reason for deletion.
- Whether an alternative implementation exists.
- Scope of impact.

It is not required to relist all functions that did not change.

## V. Data and Processing Changes

When data processing is involved, state:

- Which data was used.
- Data source.
- Data location.
- Data structure.
- Input count.
- Processing rules.
- Filtering conditions.
- Output count.
- Final result.
- Output location.

Raw data and processing records must be independently inspectable.

## VI. Call Relationship Changes

When module collaboration is involved, state:

- The original call relationships.
- The location of this change.
- The new call relationships.
- How data is passed.
- Whether upstream and downstream have changed.

Use a flow diagram where necessary.

## VII. Interfaces and Compatibility

Must make clear:

- Whether interfaces were added.
- Whether interfaces were modified.
- Whether interfaces were deleted.
- Whether the input structure changed.
- Whether the output structure changed.
- Whether fields changed.
- Whether field types changed.
- Whether the invocation method changed.
- Which modules are affected.
- Whether data migration is needed.

Even when there is no interface change, this must be stated explicitly.

## VIII. Testing and Verification

Must distinguish:

- Passed.
- Failed.
- Not executed.
- Unable to execute.
- Not applicable.

State the actual test commands, test scope, results, and failure reasons.

Tests that were not executed must not be written as passed.

## IX. Outstanding Items

List:

- Unimplemented functionality.
- Unfixed problems.
- Unfinished documentation.
- Unverified parts.
- Matters requiring further investigation.

Record them in the project's outstanding items list as well.

## X. Authenticity Requirements

The delivery report must be based on:

- Actual code differences.
- Actual file changes.
- Actual function definitions.
- Actual runtime results.
- Actual test results.
- Actual logs.

Prefer Git Diff or other version diff tools.

Existing functionality must not be described as newly added this time.

Planned modifications must not be described as already modified.

Test results must not be fabricated.

## XI. Adjusting Length According to Scale

Simple modifications may be described concisely.

Module-level development requires file and function descriptions.

Cross-module refactoring requires complete descriptions of data flow, interfaces, and compatibility.

The same information must not be repeated in order to satisfy a template.

## XII. Final Principle

The user must clearly know:

What was changed, why it was changed, how exactly it was changed, what impact it produced, and what remains unfinished.
