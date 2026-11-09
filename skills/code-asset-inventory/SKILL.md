---
name: code-asset-inventory
description: Code asset inventory and functional reuse standard. Requires checking existing modules, functions, utilities, and actual implementations before development, and building a searchable capability index.
trigger: 代码资产, 函数索引, 模块清单, 能力盘点, 重复实现, 代码复用, refactor, inventory, reuse, duplicate implementation
---

# Code Asset Inventory and Functional Reuse Standard

## I. Core Principle

Code in a project is a capability asset that can be searched, understood, and reused.

It is not enough to know which files a project has; it is also necessary to know which functions are already implemented inside those files.

Before developing a new feature, existing capabilities must be understood first.

## II. Inventory Scope

At minimum, include:

- Python scripts.
- Other program files.
- Public modules.
- Utility functions.
- Classes and methods.
- API clients.
- Data processing programs.
- Validators.
- Data models.
- Workflow nodes.
- Configuration and rule files.
- Test code.

## III. Code Asset Index

A project should maintain a unified code asset index.

Important modules should record at least:

- File path.
- Module name.
- Module responsibility.
- Main functions.
- Function purpose.
- Input parameters and types.
- Return value and structure.
- External dependencies.
- Call relationships.
- Whether it can be reused.
- Current status.

Important functions should record at least:

- Function name.
- Containing file.
- Actual function.
- Parameters.
- Return value.
- Main processing steps.
- File read/write behavior.
- Call sites.
- Whether side effects exist.

The index should preferentially have its basic information generated automatically, with business meaning added by developers.

## IV. Mandatory Search Before Development

Before adding a new implementation:

1. Inspect the relevant directories.
2. Search for similar files.
3. Search for similar functions.
4. Inspect public modules.
5. Inspect the actual function implementations.
6. Inspect existing call relationships.
7. Inspect whether existing capabilities can be combined.
8. Inspect the limitations of existing implementations.

It is forbidden to judge whether two functions are identical based only on file names or function names.

The actual implementation must be read.

## V. Reuse Priority

Decide in the following order:

1. Reuse the existing function directly.
2. Extend the existing function.
3. Combine multiple existing functions.
4. Extract common logic.
5. Only create a new implementation after confirming that reuse is impossible.

If a new implementation is decided on, it must state:

- Which existing implementations were inspected.
- Why they do not meet the requirement.
- The responsibility difference between the new implementation and the existing ones.
- Why extending the original implementation is not appropriate.

## VI. Duplicate Implementation Is Forbidden

Forbidden:

- Copying an existing function and changing only a small amount of code to form a new version.
- Implementing the same common logic separately in multiple modules.
- Concluding that functions differ in function merely because their names differ.
- Bypassing an original implementation because it is unfamiliar.
- Creating a new utility without first checking existing capabilities.

If different business scenarios genuinely require different implementations, their applicable scope and differences must be clearly stated.

## VII. Code Asset Index Updates

After adding, modifying, or deleting an important module or function:

- Update the module list.
- Update the function index.
- Update parameters and return values.
- Update call relationships.
- Update module responsibilities.
- Mark implementations that have been deprecated.

If the project already has an automatic indexing tool, it should be used preferentially.

The index must not be manually fabricated without checking the actual code.

## VIII. Pre-Completion Checks

- Were existing related modules checked?
- Were actual function implementations read?
- Were similar functions checked?
- Was reuse considered first?
- Does duplicate implementation exist?
- Does the new feature have a clear responsibility?
- Is the index consistent with the actual code?

## IX. Final Principle

Adding new code is not the default choice.

Understanding existing implementations and making full use of existing capabilities is the starting point for developing a new feature.
