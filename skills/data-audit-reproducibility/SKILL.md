---
name: data-audit-reproducibility
description: Raw data preservation, data source tracing, data processing audit, and historical execution reproducibility standard. Ensures humans can independently inspect the data and reproduce the results.
trigger: raw data, 原始数据, 数据审计, 数据来源, 数据血缘, 数据追踪, 数据转换, 数据复现, provenance, lineage, reproducibility
---

# Data Audit and Reproducibility Standard

## I. Core Principle

Data must be independently inspectable by humans.

An Agent's analysis result cannot substitute for raw data.

Final output must be traceable to real inputs and the actual processing steps.

Must guarantee:

1. Raw data has an actual storage location.
2. Raw data has not been overwritten by processing results.
3. Every significant transformation is recorded.
4. Every output can be traced back to its input source.
5. Historical executions can be identified and reproduced.
6. Humans can inspect the data without relying on the Agent's summaries.

## II. Data Lifecycle

When data processing is involved, the following process must be made explicit:

Raw data
    ↓
Data parsing
    ↓
Data normalization
    ↓
Data filtering
    ↓
Data cleaning
    ↓
Data transformation
    ↓
Data analysis
    ↓
Final output

The actual process may differ, but it must faithfully reflect the steps the program really executes.

Processing steps must not be fabricated in order to match the illustrative flow.

## III. Raw Data Preservation

Raw data must be stored separately from processing results.

The scope includes:

- Raw API responses.
- Web collection results.
- Raw JSON.
- Raw CSV.
- Raw HTML.
- Raw database exports.
- Raw files.
- User-provided raw data.
- Results returned by external tools.

Preservation requirements:

1. Preserve the complete raw content as far as possible.
2. Cleaned data must not overwrite raw data.
3. Only a statistical summary must not be stored.
4. Only Agent-summarized data must not be retained.
5. Record the raw data storage location.
6. Record the data generation time.
7. Record the source.
8. Record the file size.
9. Record the data hash.
10. Record whether the preservation is complete.

If complete preservation is impossible due to storage, privacy, or data volume limits, the limits, the truncation range, and an alternative storage location must be explicitly recorded.

Incomplete data must not be marked as complete data.

## IV. Separation of Raw Data and Processed Data

The following directory organization is recommended; existing project directories may be used as they are:

data/
├── raw/
│   └── raw inputs
├── intermediate/
│   └── intermediate processing results
├── processed/
│   └── cleaned and normalized results
├── output/
│   └── final output
└── audit/
    └── data processing records

Existing data must not be relocated repeatedly just to adopt this directory layout.

## V. Data Source Records

Every piece of significant data should record at least:

- Data name.
- Data source.
- Source file or interface.
- Retrieval time.
- Retrieval batch.
- Generating module.
- Raw file location.
- File hash.
- Data format.
- Data version.
- Data scale.

If the source is unclear, it must be marked as unknown; the source must not be guessed.

## VI. Data Transformation Records

Every significant data transformation should record at least:

- Execution ID.
- Input file.
- Input file hash.
- Output file.
- Output file hash.
- Executing function.
- Executing program version.
- Parameters used.
- Configuration used.
- Transformation rules.
- Input record count.
- Output record count.
- Excluded record count.
- Exclusion reasons.
- Execution time.
- Execution status.

It must be possible to explain how the input data became the output data.

## VII. Data Count Reconciliation

Significant processing stages should record count changes.

For example:

Raw records: 1000
Parsed successfully: 980
Parse failures: 20
Retained after filtering: 650
Excluded by filtering: 330
Final output: 650

Must be able to reconcile:

Raw count = successfully processed count + failure count

When the actual business involves splitting, merging, or duplicate records, the counting criteria must be explicitly stated.

Data must not be fabricated in order to satisfy count equality.

## VIII. Data Modification and Integrity Protection

Raw data is in principle stored read-only.

If modification is necessary:

- Retain the pre-modification version.
- Generate a new version.
- Record the reason for modification.
- Record the modifying program.
- Record the modification time.
- Record the before and after hashes.

A hash is used to check whether a file has changed; it does not mean the data content itself is correct.

## IX. Historical Execution Reproduction

Significant executions must preserve sufficient reproduction information:

- run_id.
- Input data version.
- Input data hash.
- Code version or commit ID.
- Configuration file version.
- Runtime parameters.
- Dependency versions.
- Execution environment.
- Random seed (where applicable).
- External service version or response snapshot (where applicable).
- Output location.

When reproducing, prefer historical input data rather than re-collecting.

If external services, models, or third-party data have already changed, it must be clearly stated that the historical environment cannot be fully restored.

It must not be claimed that every execution can be reproduced one hundred percent.

## X. Independent Human Audit

Humans must be able to directly inspect:

1. Raw data.
2. Data file structure.
3. Real records.
4. Processing parameters.
5. Transformation rules.
6. Filtering conditions.
7. Excluded records.
8. Final output.
9. Execution logs.
10. Data version and integrity information.

Humans must not be required to understand the data only through the Agent's explanation.

Provide direct access via CSV, JSON, database queries, or other means when necessary.

## XI. Privacy and Security

Sensitive information must receive appropriate protection.

But the following must be distinguished:
- Fields that need masking.
- Fields that can be retained normally.
- Fields that must not be persisted.
- Fields that may only be retained for a short period.

Audit information for an entire event must not be deleted merely to protect a single sensitive field.

For content that cannot be saved, the necessary source, time, operation, and limitation notes must be retained.

## XII. Acceptance Criteria

Must be able to answer:

- Where is the raw data?
- Where did the data come from?
- Is the raw data complete?
- Was the data modified?
- What processing did each step undergo?
- Which records were excluded?
- Why were they excluded?
- How was the final data generated?
- Which execution produced this result?
- Can it be re-executed using historical inputs?

When these cannot be answered, do not claim the data processing has complete audit capability.

## XIII. Final Principle

Data is fact; the Agent's interpretation is opinion.

The fact itself must be preserved so that humans retain the ability to inspect and judge independently.
