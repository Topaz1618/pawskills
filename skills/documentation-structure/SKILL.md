---
name: documentation-structure
description: Documentation structure and information organization standard. Requires establishing overall understanding first, then expanding details item by item, and finally consolidating public reference information.
trigger: 文档结构, 章节安排, 文档组织, 目录, 信息顺序, 总览, 详细说明, document structure, organization
---

# Documentation Structure and Information Organization Standard

## I. Core Principle

All documentation should follow a progression from shallow to deep.

For system, project, and module technical documentation, prefer:

**Part One: Overview**

**Part Two: Detailed Description**

**Part Three: Public Reference**

A specific document may be adjusted according to its theme, but it must not break the natural order in which the reader understands the information.

## II. Part One: Overview

First let the reader understand the complete composition.

For a system containing modules A, B, and C:

### A. Module A

Introduce:
- Module name.
- Location.
- Brief function description.
- Main responsibilities.

### B. Module B

Introduce:
- Module name.
- Location.
- Brief function description.
- Main responsibilities.

### C. Module C

Introduce:
- Module name.
- Location.
- Brief function description.
- Main responsibilities.

The overview must cover all major components.

Provide as needed:
- Overall flow diagram.
- Module relationship diagram.
- Data flow.
- Main dependency relationships.

The overview must not pile up large amounts of implementation detail ahead of time.

## III. Part Two: Item-by-Item Detailed Description

Expand in the order given in the overview.

Each module is introduced according to the actual situation:

1. Module introduction.
2. Functional responsibilities.
3. Usage scenarios.
4. Input data.
5. Input data structure.
6. Processing logic.
7. Output data.
8. Output data structure.
9. Core functions.
10. Function call relationships.
11. Upstream modules.
12. Downstream modules.
13. External dependencies.
14. Exception handling.
15. Testing and verification methods.

Different modules adopt a consistent organization method.

Inapplicable content may be omitted; content must not be fabricated for the sake of template completeness.

## IV. Part Three: Public Reference

After the reader already understands each module, introduce public content in a unified way.

Include as actually needed:

- Public data models.
- Enumeration definitions.
- Public field definitions.
- Shared interfaces.
- Public functions.
- Global configuration.
- Public exception types.
- General rules.
- Shared dependencies.

Public content must state which modules use it.

## V. Organizing Workflow Documentation

For workflow documentation, prefer:

### Part One: Overall Objective

Introduce the problem the workflow solves and its final objective.

### Part Two: Workflow Overview

Present in actual execution order:

- Each stage.
- Stage responsibilities.
- Input data.
- Output data.
- Important files.
- Relationships between modules.

### Part Three: Detailed Execution Process

Introduce the implementation of each stage in actual execution order.

## VI. Avoiding Repetition

Forbidden:

1. Creating a module summary table with identical content after the overview has already fully shown the modules.
2. Explaining the same fields repeatedly across multiple chapters.
3. Re-listing files and inputs and outputs that the flow diagram has already clearly shown.
4. Mechanically adding summary chapters for the sake of formal completeness.
5. Repeatedly introducing the same background.
6. Expressing the same concept under multiple different names.

When the detailed part needs to reference information from the overview, continue and expand from it directly rather than copying it again.

## VII. Flexible Adjustment According to Document Type

Different documents use the structure that suits them.

- API documentation: interface overview → interface details → public models.
- Data documentation: data system overview → data file details → public field definitions.
- Project documentation: project overview → module details → public reference.
- Deployment documentation: deployment overview → operational steps → parameters and reference.
- Troubleshooting documentation: problem symptoms → troubleshooting process → causes and solutions.

## VIII. Final Check

Check:

- Is the complete composition introduced first?
- Is the overall understanding established first?
- Does the detailed description expand in the order of the overview?
- Are public definitions placed in a suitable location?
- Are there any duplicate chapters?
- Is necessary information missing?
- Has redundant content been created for the sake of the template?

## IX. Final Principle

**The overview shows the whole picture, the detailed description goes deep into the implementation, and the public reference consolidates shared definitions.**

Let the reader first know what the system consists of, then understand how each part works, and finally consult the shared definitions.

Information should be fully expressed once, in the most appropriate location.
