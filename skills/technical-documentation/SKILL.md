---
name: technical-documentation
description: Project-wide technical documentation quality standard. Ensures documentation is based on real code and data, has complete context, clear logic, accurate descriptions, and maintainability.
trigger: 技术文档, 文档编写, 文档更新, 文档审核, 接口文档, 数据文档, 部署文档, 术语规范, 抽象术语, 实体, documentation, technical writing, terminology, entity, naming
---

# Project-Wide Technical Documentation Standard

## I. Core Principle

The primary goal of technical documentation is to let readers accurately understand what the project actually is, how it works, and what the relationships between its components are.

Documentation must not be merely a listing of code, functions, fields, and technical terminology.

It must achieve the following:

1. Introduce the background before introducing details.
2. Build the overall understanding before introducing local parts.
3. Explain what an object is before explaining how it works.
4. Explain the purpose before explaining the implementation.
5. Explain the data source before explaining data processing.
6. Explain the relationships between objects before introducing their respective details.
7. Provide necessary explanation when a new concept first appears.
8. Keep terminology and definitions consistent throughout.
9. Base all technical statements on the actual implementation.

## II. Organizing Content According to Document Type

Different documents must not mechanically apply the same template.

### 2.1 System and Module Documentation

Introduce:
- Background and objectives.
- Overall composition.
- Responsibilities of each module.
- File locations.
- Module relationships.
- Overall execution flow.
- Detailed description of each module.
- Public data models and interfaces.
- Known limitations.

### 2.2 API and Interface Documentation

Introduce:
- Purpose of the interface.
- List of interfaces.
- Request method.
- Call conditions.
- Request parameters.
- Data structure.
- Response structure.
- Field constraints.
- Error codes.
- Exception handling.
- Call examples.
- Permissions and compatibility.

Must distinguish the designed interface, the actual request, and the real response.

### 2.3 Data and Data Processing Documentation

Introduce:
- Overview of the data system.
- Data sources.
- Data storage locations.
- Raw data structure.
- Data flow.
- Field definitions.
- Data cleaning and filtering rules.
- Data transformation process.
- Actual data samples.
- Data quality.
- Downstream usage.

### 2.4 Deployment and Runtime Documentation

Introduce:
- Applicable environments.
- Dependency requirements.
- Installation steps.
- Configuration method.
- Startup method.
- Parameter descriptions.
- Runtime results.
- Log locations.
- Stopping and recovery.
- Troubleshooting.

Must provide genuinely operable steps.

### 2.5 Troubleshooting Documentation

Introduce:
- Problem symptoms.
- Scope of impact.
- Conditions that trigger the problem.
- Confirmed facts.
- Pending verification speculations.
- Troubleshooting process.
- Original errors.
- Root cause.
- Solutions.
- Verification results.
- Preventive measures.

### 2.6 Technical Design Documentation

Introduce:
- Requirement background.
- Problem definition.
- Goals and non-goals.
- Current system situation.
- Design approach.
- Module responsibilities.
- Data structures.
- Interface design.
- Exception handling.
- Compatibility.
- Testing criteria.
- Risks and limitations.

## III. Context Continuity

When introducing an important object for the first time, the following should be stated:

- What it is.
- Which module it belongs to.
- Where it comes from.
- What problem it solves.
- Why it exists.
- What relationship it has with other objects.

Introducing files, functions, fields, or abbreviations without background is forbidden.

## IV. Authenticity Requirements

Documentation must distinguish:

- Design proposals from actual implementations.
- Code definitions from actual runtime behavior.
- Planned outputs from actual outputs.
- Implemented from unimplemented.
- Tested from untested.
- Confirmed from pending verification.

Files referenced must have their actual content checked.

Functions referenced must have their actual implementation checked.

Call relationships referenced must have their real call sites checked.

Data referenced must be actually read.

Runtime results referenced must have real execution records.

## V. Data Sample Requirements

Data examples in documentation must be clearly labeled as:

- Real data samples.
- Masked data samples.
- Manually constructed illustrative examples.

Manually constructed examples must not be passed off as real data.

## VI. Documentation and Code Synchronization

Before modifying documentation:

1. Check the related code.
2. Check the related files.
3. Check the existing documentation.
4. Confirm the real interfaces.
5. Confirm the data structures.
6. Confirm the call relationships.

After modifying documentation:

1. Check the paths.
2. Check the function names.
3. Check the field names.
4. Check the inputs and outputs.
5. Check the call relationships.
6. Check for outdated content.
7. Check other affected documentation.

The entire documentation system must not be rewritten pointlessly for a local modification.

## VII. Documentation Quality Review

After each important document is completed, check:

### Structure
Is the overall understanding established before details are introduced?

### Context
Are there new concepts that lack explanation?

### Completeness
Is information necessary for understanding and use missing?

### Authenticity
Is it consistent with the real code and data?

### Readability
Is there repetition, piling up, or obscure expression?

Defects that affect understanding must be corrected.

## VIII. Final Delivery

State:

- Which documents were created or modified.
- The purpose of each document.
- The main content changes.
- Whether real code and data were checked.
- Whether context continuity was checked.
- Whether inconsistencies with the implementation were found.
- Which content remains unverified.
- Whether there are pending items.

## IX. Natural and Accurate Engineering Language

All technical documentation must use engineering expressions that developers recognize and that carry a single unambiguous meaning.

Terminology must never be invented, abstracted, or embellished in order to appear more professional.

### 9.1 Abstract Terms Must Not Be Overused

When describing ordinary file data, it is forbidden to call a record in a JSON file, or a row in a CSV file, an "entity" without justification.

Prefer:

- Data record.
- JSON record.
- CSV data row.
- Data structure.
- Field.
- File.
- Data model.

The term "entity" is permitted only when the subject genuinely involves a business entity, a database entity, or a design with explicit entity semantics.

An abstract concept from one area must not be promoted into a project-wide uniform term.

### 9.2 Name Actual Files

When describing input and output, the reader must be able to tell at a glance which real files are being discussed.

Prefer:

- Reads the file.
- Input file.
- Generated file.
- Output file.
- Intermediate file.
- File save path.
- File content.

Avoid substituting abstract phrases such as "input", "output", "data artifact", or "data consumer" for a concrete statement.

Example — not recommended:

Output: `data/example.json`

Recommended:

**Generated file:** `data/example.json`

Purpose: stores the keyword collection plan generated by this run.

### 9.3 Data Structures Must Show a Complete Example

It is forbidden to consider a data structure explained by writing only:

`array<SomeRecord>`, `object<SomeModel>`, or any other abstract type declaration.

A concrete code block in the real format must be provided directly.

For JSON, show at least:

- The top-level structure.
- The complete field hierarchy.
- Field names.
- The data type of each field.
- The structure of nested objects and arrays.

Then explain the fields one by one.

For CSV, show the actual header row and representative data rows.

For JSONL, show an actual single-line record.

For a database, show the table structure together with the necessary field definitions.

Examples must clearly distinguish between:

- A structural example.
- A real sample taken from the current file.
- The actual result produced by a run.

A manually constructed example must never be passed off as real data.

### 9.4 Natural Technical Document Expression

Prefer specific and direct phrasing.

Avoid:

- Unnecessary conceptual packaging.
- Invented terminology.
- English nouns used without context.
- Abstract expressions adopted only to appear professional.
- Type declarations substituted for actual data display.
- A field table used in place of a complete data structure description.

Where a technical term is genuinely necessary, the original code name may be kept, but it must be explained the first time it appears.

### 9.5 Terminology Rules

1. Ordinary data objects, JSON records, and CSV data rows must not be called "entities".
2. An `Object` in program code is described as an "object".
3. One actual piece of data in a file is described as a "data record".
4. Fields and their nesting relationships are described as a "data structure".
5. "Entity" is used for a business entity in a database only when the subject genuinely involves domain entity modeling, and its business meaning must be stated explicitly.
6. Abstract terminology that the project does not already use must not be created, promoted, or introduced.
7. Prefer terminology common to the programming language, the project code, and established engineering practice.

**Principle: use the name the code uses, and explain accurately what it is. Do not invent a conceptual system for the sake of writing documentation.**

### 9.6 Final Review

When the document is complete, check:

1. Are ordinary data records unnecessarily called entities?
2. Do abstract terms appear that carry no concrete meaning?
3. Is only a type declaration given, with no real data structure shown?
4. Are the files actually read and generated named explicitly?
5. Are any expressions used that a developer would not recognize, or that invite ambiguity?
6. Could the same technical content be expressed more directly?

**Final requirement: when it is possible to name the file, do not talk about a "data artifact"; when it is possible to name a data record, do not invent an abstract concept; when it is possible to show the actual JSON, do not give only a type name. Technical documentation should help developers understand the engineering, not require them to first understand terminology the author invented.**

---

## X. Final Principle

Documentation is not about demonstrating how many technical terms the author knows.

Documentation is a tool that enables other people to accurately understand and maintain a real engineering project.
