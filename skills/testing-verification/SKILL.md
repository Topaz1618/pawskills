---
name: testing-verification
description: Software testing and independent verification standard. Requires that tests are genuinely executed, results are inspectable, failures are not hidden, and the verification scope is explicit.
trigger: 测试, 验证, 调试, bug, QA, unit test, integration test, regression, verification, acceptance
---

# Testing and Verification Standard

## I. Core Principle

The completion of code writing does not mean the functionality is correct.

The ability of a program to run does not mean the result is correct.

The existence of test code does not mean the test has been executed.

A passing test must be based on real execution results.

## II. Test Types

Select according to the task:

### 1. Unit Tests

Verify the input, processing, and output of a single function or component.

### 2. Integration Tests

Verify the data transfer and call relationships between multiple modules.

### 3. Interface Tests

Verify request format, response structure, field types, and exceptional behavior.

### 4. Data Quality Tests

Verify data counts, fields, types, null values, uniqueness, and business constraints.

### 5. Regression Tests

Verify that the current change did not break existing functionality.

### 6. End-to-End Tests

Verify that a complete business flow runs correctly.

Executing every test type irrelevant to the current task purely for form is not acceptable.

## III. Must Be Clarified Before Testing

Every significant test must state:

- Test objective.
- Test target.
- Test input.
- Test data source.
- Expected result.
- Pass criteria.
- Failure criteria.

Test data must be clearly distinguished as:

- Real production data.
- Masked data.
- Manually constructed test data.
- Mock data.

Mock results must not be described as real production environment results.

## IV. Test Execution Requirements

Tests must actually be executed.

Record:

- Test command.
- Execution time.
- Environment used.
- Data used.
- Input parameters.
- Actual output.
- Exit status.
- Failure messages.
- Test report location.

Claiming a test passed based only on reading the test code is not acceptable.

## V. Test Result Classification

Must clearly distinguish:

- PASS: actually executed and passed.
- FAIL: actually executed but failed.
- BLOCKED: could not be executed due to environment or dependency issues.
- NOT_RUN: not executed.
- NOT_APPLICABLE: not applicable to the current task.

Writing BLOCKED or NOT_RUN as PASS is forbidden.

## VI. Failure Handling

When a test fails:

1. Preserve the original error.
2. Check the failure location.
3. Check the input data.
4. Check the actual output.
5. Analyze the cause of the failure.
6. Fix the related problem.
7. Re-run the necessary tests.

Passing results must not be manufactured by deleting failing tests, skipping tests, or changing expected values.

If the test itself is problematic, this must be clearly stated and the test basis corrected.

## VII. Test Coverage Scope

Determine according to the impact scope of the change:

- Single function change: test the related function.
- Module change: test the module and its direct dependencies.
- Interface change: test caller compatibility.
- Cross-module change: test the complete data chain.
- Data processing change: test data counts and field changes.
- Logging change: inspect the actually generated logs.

## VIII. Test Data Protection

Tests must not modify or delete real production data without authorization.

Prefer an independent test directory, a temporary database, or an isolated environment.

After testing, clearly state:

- Whether files were produced.
- Whether data was modified.
- Whether temporary resources were cleaned up.
- Whether test results were retained.

## IX. Independent Review

For significant changes, a review separated from the implementation process should be conducted.

Review focus:

- Whether the original requirement is satisfied.
- Whether new problems were introduced.
- Whether boundary conditions were missed.
- Whether existing interfaces were affected.
- Whether untested paths exist.
- Whether data inconsistency exists.
- Whether unnecessary duplicate implementation exists.

Review conclusions must have a basis.

## X. Final Delivery

State:

- Which tests were actually executed.
- Which tests passed.
- Which tests failed.
- Which tests were not executed.
- Why they were not executed.
- What risks remain.
- Where the test results are stored.

## XI. Final Principle

Testing verifies actual behavior; it is not a means of finding support for the Agent's claims of completion.

Without verification, do not claim that verification has been performed.
