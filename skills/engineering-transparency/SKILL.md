---
name: engineering-transparency
description: Engineering transparency standard. Requires all development work to have clear file responsibilities, function responsibilities, data flow, module relationships, and inspectable implementation descriptions.
trigger: 透明化, 黑盒, 可追溯, 文件职责, 函数说明, 数据结构, 模块关系, 工程审计, transparency, traceability
---

# Engineering Transparency Standard

## I. Core Principle

Code is not the only deliverable.

A feature is truly complete only when a developer can understand:

- What it does.
- Which files it consists of.
- What each file is responsible for.
- What each important function is responsible for.
- Where the data comes from.
- What processing the data goes through.
- What the final result is.
- How modules connect to each other.
- How actual behavior is verified.

An implementation that cannot be understood, cannot be traced, and cannot be verified must not be treated as a complete delivery.

## II. Before Development: Understand the Existing Engineering

Before starting development, the engineering related to the task must be inspected:

1. Relevant directory structure.
2. Existing file responsibilities.
3. Existing modules and public functions.
4. The actual implementation of related functions.
5. Call relationships among related modules.
6. Where the real data is stored.
7. The actual structure of the data.
8. Upstream and downstream modules.
9. Existing tests and documentation.

Responsibilities must not be inferred from file names alone.

New implementations must not be created without first checking existing capabilities.

## III. File Transparency

When adding, modifying, or deleting files, the following must be stated:

| Item | Content |
|---|---|
| File path | Complete relative path |
| File type | Python, JSON, Markdown, etc. |
| File responsibility | What it is actually responsible for |
| Input | What it receives |
| Output | What it produces |
| Upstream | Who calls or generates it |
| Downstream | Who uses it |
| Dependencies | Which modules or external libraries it uses |
| Reason for change | Why it was added, modified, or deleted |

Only the files involved in this change and their necessary context need to be described.

Large projects may provide a relevant directory tree; there is no need to print the entire project pointlessly.

## IV. Function Transparency

Important functions that are added, modified, or deleted must have the following stated:

1. Function name.
2. Containing file.
3. Function responsibility.
4. Parameter names.
5. Parameter types.
6. Parameter meanings.
7. Required parameters and default values.
8. Return value type.
9. Return value structure.
10. Main processing steps.
11. Other functions called.
12. File read/write behavior.
13. Exception handling.
14. Which modules call it.

Providing only the function name is not acceptable.

The description must be based on the actual code; functionality must not be inferred from function naming.

## V. Data Transparency

When data processing is involved, the following must be stated:

- Data source.
- Data storage location.
- Actual data structure.
- Field types.
- Field meanings.
- Input count.
- Processing rules.
- Data transformation.
- Filtering conditions.
- Excluded count.
- Final output.
- Output storage location.

Raw data preservation and processing audit follow data-audit-reproducibility.

Execution records follow production-logging.

## VI. Call Relationship Transparency

Must state:

- Who calls whom.
- Where the input comes from.
- Which functions the data passes through.
- Which modules modify the data.
- Who generates the output.
- Who consumes it downstream.
- How failures propagate.

When multiple modules are involved, use a flow diagram consistent with the actual code.

Example:

Data collection module
    ↓
Raw data file
    ↓
Parsing module
    ↓
Normalization module
    ↓
Analysis module
    ↓
Result output module

The above is only a structural illustration; the actual flow must follow the project implementation.

## VII. Engineering Documentation Synchronization

After significant engineering changes, update as appropriate:

- PROJECT_STRUCTURE.md
- MODULES.md
- FUNCTIONS.md
- DATA_DICTIONARY.md
- DATA_FLOW.md
- CHANGELOG.md

These are recommended documentation responsibilities; every project is not required to mechanically create six files.

When the project already has equivalent documentation, maintain the existing documentation preferentially.

## VIII. False Transparency Is Forbidden

Forbidden:

- Fabricating real data samples.
- Fabricating function call relationships.
- Guessing functionality from file names.
- Giving only file names without explaining responsibilities.
- Giving only function names without explaining logic.
- Describing planned implementations as already implemented.
- Describing unverified functionality as verified.
- Introducing only the final output without explaining data sources.
- Using abstract terminology to conceal the actual implementation.

When something cannot be confirmed, explicitly state:

- Not checked.
- Not confirmed.
- Not implemented.
- Not verified.

## IX. Final Acceptance

Without opening the source code, a developer should be able to understand from the engineering documentation and related data records:

1. The actual effect of the feature.
2. The file organization.
3. Function responsibilities.
4. Input and output structures.
5. The data processing steps.
6. Module call relationships.
7. Dependency relationships.
8. How to test.
9. The actual changes made.

For low-level details that can only be confirmed by reading source code, accurate code locations should be provided; do not pretend the documentation already covers everything.

## X. Final Principle

Engineering transparency is not about making the Agent write more text.

It is about giving the engineering itself a clear structure, explicit responsibilities, inspectable data, and real execution records.
