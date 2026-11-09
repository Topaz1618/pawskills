---
name: data-first-execution
description: Data-first execution policy. Requires checking existing data, historical results, and execution records first, avoiding unjustified re-collection, recomputation, and re-execution.
trigger: 数据, 分析, 统计, 采集, 爬取, 重跑, 重算, 验证, data, analysis, statistics, collection, rerun, recompute
---

# Data-First Execution Policy

## I. Core Principle

**Existing data takes priority over re-execution, and existing conclusions take priority over repeated computation.**

Before performing any data analysis, statistics, collection, transformation, or business judgment, existing data and historical execution results must be checked first.

It is forbidden to use repeated execution in place of analysis and judgment.

## II. Required Checks Before Execution

### 1. Inspect Existing Data

Check:
- Raw data files.
- Processed data files.
- Intermediate data files.
- Database records.
- Historical export files.
- Caches.
- Temporary data.
- Generated analysis results.

### 2. Inspect Historical Analysis

Confirm:
- Whether the same analysis has already been executed.
- Whether statistics results already exist.
- Whether analysis reports have already been generated.
- Whether directly reusable intermediate results exist.
- Whether the data version used by the historical results conforms to the current task.

### 3. Inspect Historical Execution Records

Confirm:
- Whether related tasks have been executed before.
- Which data was used.
- When it was executed.
- Whether it succeeded.
- Where the output files are.
- Whether there are failure or partial completion records.

### 4. Inspect Whether the Data Is Applicable

The existence of a file does not mean the data is usable.

Must check:
- Data source.
- Data version.
- Update time.
- Field structure.
- Data volume.
- Data completeness.
- Whether it conforms to the current analysis scope.

## III. Execution Decision

| Current Situation | Correct Handling |
|---|---|
| Existing data is complete and applicable | Use it directly |
| Existing data is sufficient but not yet analyzed | Analyze based on existing data |
| Only partial data exists | Supplement only the missing portion |
| Historical results can be reused | Reuse them directly |
| Data structure has changed | Check the impact of the change, then decide |
| Data is outdated | State the basis for it being outdated, then decide whether to update |
| Data is corrupted | Locate the extent of corruption and repair locally where possible |
| Data does not match the current task | State the mismatch |

## IV. Unjustified Repeated Execution Is Forbidden

Forbidden:

1. Re-collecting without first checking existing data.
2. Re-collecting all data when complete data already exists.
3. Repeatedly recomputing analysis results without reason when they already exist.
4. Re-running the entire pipeline to verify a single local issue.
5. Repeatedly running the program merely because the result is uncertain.
6. Repeatedly calling a successful interface without checking historical records.
7. Assuming a program should be re-run merely because it is runnable.

## V. Distinguish Missing Data from Being Outside the Collection Scope

The absence of a certain item in the data does not necessarily mean re-collection is required.

Must determine:
- Does the current task require that item to be included?
- Does the original collection scope cover it?
- Do the collection conditions allow it to be obtained?
- Did historical data genuinely omit it?
- Is the absence in the current data itself a valid result?

The collection scope must not be expanded merely to make the data look more complete.

## VI. Incremental Execution Principle

When data genuinely needs to be supplemented:

1. Clarify the existing data.
2. Clarify the missing data.
3. Clarify the reason for the absence.
4. Clarify the supplementation operation.
5. Execute only the necessary incremental task.
6. Distinguish newly added data from historical data.
7. Verify the merged result.

Existing data must not be overwritten without reason.

## VII. Data Version Management

Every significant data processing operation should record:

- Data source.
- Data version or file hash.
- Data generation time.
- Data processing program version.
- Configuration used.
- Processing parameters.
- Final output version.

When historical data changes, the difference between the old and new versions should be identifiable.

## VIII. Output Requirements

At the end of every data task, state:

1. Which existing data was used.
2. Which historical results were reused.
3. Whether new collection was performed.
4. Whether new computation was performed.
5. Why these new operations were necessary.
6. The actual execution scope.
7. The final output location.
8. Which conclusions still lack data support.

## IX. Highest Principle

Do not keep executing operations in order to appear productive.

First understand the existing results, then determine what is genuinely missing, and finally execute the minimum necessary operation.
