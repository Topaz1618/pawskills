---
name: interface-contract
description: Engineering interface contract standard. Unifies input, output, field types, invocation method, exception handling, and compatibility between modules.
trigger: 接口, 输入输出, 数据结构, 模块开发, 新建模块, 新增脚本, 上下游, API, interface, contract, integration
---

# Engineering Interface Contract Standard

## I. Core Principle

No module may have only an implementation and no interface.

No module may have only an output and no format definition.

No downstream module may complete development by guessing the upstream data structure.

There must be explicit, stable, and verifiable interface contracts between modules.

## II. Module Responsibilities Must Be Defined Before Development

Clarify:

1. What problem the module solves.
2. Which work the module is responsible for.
3. Which work does not belong to that module.
4. Who provides the data upstream.
5. Who uses the results downstream.
6. Whether reusable existing modules exist.

It is forbidden to place unrelated responsibilities into a single module.

## III. Input Contract

Must make clear:

- Input source.
- Input format.
- Input structure.
- Required fields.
- Optional fields.
- Field types.
- Field meanings.
- Whether null is allowed.
- Default values.
- Enumeration ranges.
- Data constraints.
- How missing fields are handled.
- How invalid input is handled.

Must distinguish:
- Field not provided.
- Field value is null.
- Empty string.
- Empty array.
- Empty object.
- Type error.

These cases must not be treated as identical without prior definition.

## IV. Output Contract

Must make clear:

- Output content.
- Output format.
- Output location.
- Field names.
- Field types.
- Field meanings.
- Required and optional rules.
- Data status.
- Error message structure.
- How downstream reads it.

Output formats should preferentially follow the project's existing conventions.

Existing field names and types must not be changed without authorization.

## V. Invocation Contract

Clarify:

- Invocation entry point.
- Invocation parameters.
- Parameter types.
- Default values.
- Execution method.
- Success return value.
- Failure return value.
- Timeout handling.
- Retry strategy.
- External dependencies.
- Whether batch processing is supported.

## VI. Module Responsibility Boundaries

Each module is responsible only for the work within the agreed scope.

For example:

- A collection module is responsible for obtaining raw data.
- A parsing module is responsible for parsing data.
- A normalization module is responsible for unifying data formats.
- An analysis module is responsible for computation and judgment.
- An output module is responsible for producing the final results.

The specific responsibilities are determined by the actual project architecture.

Multiple modules must not separately maintain the same set of business rules.

## VII. Field Consistency

The same category of data should preferentially use unified field names and data types.

If conversion is genuinely needed:

1. Clarify the original field.
2. Clarify the target field.
3. Clarify the conversion rule.
4. Clarify which module is responsible for it.
5. Clarify whether the original value is retained after conversion.

Each downstream module must not implement field conversion on its own.

## VIII. Interface Changes

Before modifying an existing interface, must:

1. Search for all callers.
2. Check input data sources.
3. Check output data consumers.
4. Assess field changes.
5. Assess type changes.
6. Assess compatibility.
7. Determine the migration plan.

Compatible extension is preferred.

Fields must not be deleted or types changed directly without assessment.

### 8.1 Existing Field Names Must Not Be Renamed on the Agent's Initiative

An existing field name must not be changed on the agent's own initiative.

Where historical data, interface compatibility, or a database migration is involved, the impact must be analyzed and a proposal put forward first, covering:

1. Which callers, data sources, and consumers are affected.
2. Whether historical data must be migrated, and how.
3. Whether a compatibility window is needed for external consumers.
4. Whether the two names must be carried simultaneously, and for how long.
5. How the migration is verified.

A name that is unclear may still be retained. A clearer name does not by itself authorize a rename.

### 8.2 Relationship to Naming Rules

How a new name is chosen is governed by `language-expression`, section IX, which forbids arbitrary abbreviation and compressed naming. Whether an existing name may be changed is governed by this section.

## IX. Exception Contract

Exceptions must clearly distinguish:

- Input validation failure.
- Business rule violation.
- External service failure.
- Data parsing failure.
- File read/write failure.
- Database operation failure.
- Internal program error.

Exceptions should preserve the original cause and provide an identifiable error type.

Real errors must not be masked by returning empty data.

## X. Interface Verification

Must verify:

- Normal input.
- Missing fields.
- Empty data.
- Invalid types.
- Boundary values.
- Normal output.
- Exceptional output.
- Upstream and downstream compatibility.

## XI. Final Principle

A module must not only be able to run independently; it must also be callable correctly by other modules.

An interface is not a supplementary explanation after development is complete, but an agreement that must be defined before development begins.
