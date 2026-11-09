---
name: production-logging
description: Production logging standard. Requires recording real execution facts, raw requests and responses, exceptions, data changes, and the complete execution path.
trigger: log, logging, logger, 日志, 排错, trace, audit, 运行记录, 请求记录, 错误记录
---

# Production Logging Standard

## I. Core Principle

**Log records facts; Report describes conclusions.**

The log is responsible for recording what actually happened.

The report is responsible for interpreting and summarizing the log.

The two must be kept separate.

Production logs are not work reports, not the Agent's execution summaries, and not descriptions generated to make the user feel comfortable.

## II. Decorative Logging Is Forbidden

Production logs must not contain:

- Emoji.
- Decorative headings.
- Promotional wording.
- Emotional descriptions.
- Vague success summaries.
- Agent-self-polished execution results.

The following are forbidden:

- Execution successful!
- Data retrieval successful!
- Perfectly completed!
- All processes normal!

Replace them with concrete structured events:

event=api_response_received
status=success
status_code=200
record_count=100

Emoji may appear in user-facing interfaces, but must not serve as status markers in production logs.

## III. Log Authenticity

Logs must be produced by the actually running program, the logging component, or external system results.

Forbidden:

1. The Agent fabricating logs after the fact from memory.
2. The Agent writing its own speculation as an execution fact.
3. Replacing real execution records with reporting content.
4. Modifying original errors to produce a better-looking output.
5. Hiding failures, empty results, and fallback paths.
6. Recording operations that were not executed as executed.

## IV. Structured Logging

Structured JSON logging is preferred.

Each significant log entry should contain applicable fields:

- timestamp
- level
- event
- run_id
- request_id
- trace_id
- stage
- operation
- source
- status
- duration_ms
- error_type
- error_message

Field names must remain stable.

The same concept must not be represented by different fields in different modules.

## V. Execution Identity

Every independent task must generate a unique run_id.

All stages, calls, and operations within the same task must be correlatable through the run_id.

Add as needed:

- request_id
- trace_id
- parent_run_id
- stage
- operation_id

Logs from different tasks must not be mixed together in a way that makes their origin indistinguishable.

## VI. Request Logging

All significant external requests must record:

- Request time.
- Target service.
- Request URL.
- HTTP method.
- Request parameters.
- Request headers (sensitive fields masked).
- Request body.
- Timeout settings.
- Retry strategy.
- Request ID.

Recording only "called the search API" is not acceptable.

The actual request content, or structured information sufficient to reconstruct the request, must be retained.

## VII. Response Logging

Must record:

- Response time.
- HTTP status code.
- Response headers (where applicable).
- Raw response content or its storage location.
- Response file hash.
- Response size.
- Returned record count.
- Parse status.
- Parse errors.

Must distinguish:

raw_response
parsed_response
normalized_data
filtered_data
final_output

The raw response must not be overwritten by the parse result.

Large responses may be saved as separate files, in which case the log records the file path, hash, size, and integrity status.

Recording only a response summary while losing the raw response is not acceptable.

## VIII. Data Processing Logging

Significant data transformations must record:

- Input data source.
- Input record count.
- Processing rules.
- Processing function.
- Output record count.
- Excluded record count.
- Exclusion reasons.
- Output location.
- Execution duration.

Recording only "data processing complete" is not acceptable.

## IX. Exception Logging

When an error occurs, must retain:

- Original error type.
- Original error message.
- Full stack trace (where applicable).
- File path.
- Code location.
- Current execution stage.
- Relevant input.
- Upstream call information.
- Retry count.
- Final status.

An easier-to-read error description may be added, but it must not replace the original error.

## X. Empty Result Logging

An empty result is also a valid execution fact.

Must record:

- Actual query.
- Query source.
- Query conditions.
- Returned count.
- Empty result status.
- Query duration.

Silently ignoring a query that returned no results is forbidden.

## XI. Resource Mutation Logging

When resources change, record:

- resource
- resource_id
- before
- after
- delta
- reason
- operation
- status

This applies to files, databases, caches, balances, counters, and other significant resources.

## XII. Execution Path

Must explicitly record:

- Primary path.
- Fallback path.
- Retry.
- Degradation.
- Mock.
- Stub.
- Default value substitution.
- Data source switching.

For example:

Database query failed
    ↓
Cache query
    ↓
Cache returned a result
    ↓
Task continued execution

Recording only "data loaded successfully" is not acceptable.

## XIII. Relationship Between Logs and Raw Data

Logs do not necessarily retain all large raw data, but they must be able to locate the raw data.

The log should record at least:

- File path or object identifier.
- Hash.
- File size.
- Data source.
- Preservation status.
- Integrity status.

Raw data preservation requirements are also governed by data-audit-reproducibility.

## XIV. Sensitive Data Protection

Directly recording the following is forbidden:

- Passwords.
- API Keys.
- Access Tokens.
- Secrets.
- Private authentication information.

They must be handled through an explicit masking or hashing strategy.

Masking must not destroy the non-sensitive context needed for troubleshooting.

## XV. Log Verification

After modifying the logging system, the relevant pipeline must actually be run.

Check:
- Whether requests are genuinely recorded.
- Whether raw responses are preserved.
- Whether empty results are recorded.
- Whether errors are complete.
- Whether stack traces are preserved.
- Whether data transformations are recorded.
- Whether file paths are correct.
- Whether execution IDs are correlated.
- Whether fallback paths are exposed.
- Whether Emoji appear in production logs.

Reviewing only the logging code does not mean the logging has been verified.

## XVI. Final Principle

Never substitute a summary for facts.

Never hide failures.

Never lose important data sources.

Never treat the Agent's interpretation as a real execution record.

The log must enable developers to independently reconstruct what actually happened.
