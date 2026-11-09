# Audit Data Model

The concrete record structures behind [`data-audit-reproducibility`](../skills/data-audit-reproducibility/SKILL.md).

The standard states the obligations. This document states the shape of the records that satisfy them. Use it as a reference when deciding what a record must contain; use the standard when deciding whether the record must exist at all.

All examples are illustrative. Field names may be adapted, but the required information must survive the adaptation.

---

## 1. Directory Layout

```
data/
├── raw/           # unmodified content exactly as obtained
├── intermediate/  # intermediate processing results
├── processed/     # cleaned, normalized, analysis-ready results
├── output/        # final deliverables
└── audit/         # the records that make the above auditable
```

### Rules

1. `raw/` is written once and never modified. Corrections go to a new file, not to an edit of the original.
2. `processed/` must never contain raw content that has been silently altered in place.
3. `audit/` holds records about the data, not the data itself.
4. Existing project layouts may be used as they are. A layout that satisfies the rules above does not need to be reorganized.

---

## 2. Record Types

Six record types cover the full lifecycle. Each is described with the fields it must carry.

### 2.1 Source Record — `source.json`

Describes where a piece of raw data came from.

| Field | Required | Description |
|---|---|---|
| `data_name` | yes | Human-readable identifier, unique within the run |
| `source_type` | yes | `api`, `web`, `file`, `database`, `user`, `tool`, `generated` |
| `source_locator` | yes | URL, path, or connection reference |
| `retrieved_at` | yes | ISO 8601 timestamp with timezone |
| `retrieval_batch` | yes | Identifier of the collection run |
| `generator` | yes | Module or command that produced the data |
| `raw_location` | yes | Path to the stored raw file, relative to the repo root |
| `sha256` | yes | Hash of the raw file as stored |
| `file_size_bytes` | yes | Size of the raw file |
| `format` | yes | `json`, `csv`, `html`, `parquet`, `binary`, … |
| `version` | yes | Data version identifier |
| `record_count` | when countable | Number of records contained |
| `preservation` | yes | `complete`, `truncated`, or `sampled` |
| `preservation_note` | if not complete | What was lost and why |
| `source_confidence` | yes | `confirmed`, `inferred`, or `unknown` |

`source_confidence` exists because "we are not sure where this came from" must be recorded as a fact, not resolved by a plausible guess.

#### Example

```json
{
  "data_name": "product_listings_2026_11",
  "source_type": "api",
  "source_locator": "https://api.example.com/v2/listings?page=1..40",
  "retrieved_at": "2026-11-09T14:03:11+08:00",
  "retrieval_batch": "batch-20261109-01",
  "generator": "scripts/collect_listings.py",
  "raw_location": "data/raw/listings/batch-20261109-01/page_01.json",
  "sha256": "9f2c1a...",
  "file_size_bytes": 481233,
  "format": "json",
  "version": "2026-11-09T14:03:11+08:00",
  "record_count": 1200,
  "preservation": "complete",
  "source_confidence": "confirmed"
}
```

### 2.2 Transformation Record — `transform.json`

Describes one significant transformation step.

| Field | Required | Description |
|---|---|---|
| `run_id` | yes | Identifier of the execution that performed it |
| `step_name` | yes | Short identifier of the step |
| `input_files` | yes | Paths, each with its `sha256` |
| `output_files` | yes | Paths, each with its `sha256` |
| `executed_by` | yes | Function or script name |
| `code_version` | yes | Commit, tag, or recorded hash set |
| `parameters` | yes | Runtime parameters as passed |
| `config` | yes | Configuration as used |
| `rules` | yes | The transformation rules, in a form a person can check |
| `input_count` | yes | Records read |
| `output_count` | yes | Records written |
| `excluded_count` | yes | Records deliberately dropped |
| `exclusion_reasons` | yes | Count per reason |
| `excluded_sample` | recommended | Example records for each reason |
| `started_at` | yes | ISO 8601 timestamp |
| `finished_at` | yes | ISO 8601 timestamp |
| `status` | yes | `success`, `partial`, or `failed` |
| `error` | if failed | The actual error text |

`rules` is written for a reader, not for a machine. "Drop rows where `price` is null" is a rule. "Cleaning" is not.

#### Example

```json
{
  "run_id": "run-20261109-1420",
  "step_name": "normalize_listings",
  "input_files": [
    {"path": "data/raw/listings/batch-20261109-01/page_01.json", "sha256": "9f2c1a..."}
  ],
  "output_files": [
    {"path": "data/processed/listings/2026-11-09/listings.json", "sha256": "41ab77..."}
  ],
  "executed_by": "pipeline.normalize.normalize_listings",
  "code_version": "7c1f2a9",
  "parameters": {"currency": "USD", "locale": "en-US"},
  "config": "config/pipeline/listings.yaml",
  "rules": [
    "Cast `price` to a number; rows that cannot be parsed are excluded with reason unparseable_price",
    "Normalize `title` to lower case and collapse whitespace",
    "Map `seller_country` codes to ISO 3166-1 alpha-2"
  ],
  "input_count": 1200,
  "output_count": 1154,
  "excluded_count": 46,
  "exclusion_reasons": {
    "unparseable_price": 41,
    "missing_seller_country": 5
  },
  "excluded_sample": [
    {"id": "L-00912", "price": "n/a"}
  ],
  "started_at": "2026-11-09T14:20:02+08:00",
  "finished_at": "2026-11-09T14:20:07+08:00",
  "status": "success"
}
```

### 2.3 Count Reconciliation Record — `reconciliation.json`

Records how counts changed across the stages of one run.

| Field | Required | Description |
|---|---|---|
| `run_id` | yes | Identifier of the execution |
| `stages` | yes | Ordered list of stages |
| `reconciled` | yes | Whether the arithmetic closes at every stage |
| `discrepancies` | if not reconciled | Where and how much it does not close |
| `counting_criteria` | yes | What counts as one record, and how splits/merges are treated |

Counting criteria are required because a run that splits one record into three, or merges three into one, will not balance unless the basis is stated.

#### Example

```json
{
  "run_id": "run-20261109-1420",
  "stages": [
    {"stage": "raw", "count": 1200},
    {"stage": "parsed", "count": 1200, "failed": 0},
    {"stage": "normalized", "count": 1154, "excluded": 46},
    {"stage": "output", "count": 1154}
  ],
  "reconciled": true,
  "counting_criteria": "One record is one listing page entry. No splits or merges occurred in this run."
}
```

### 2.4 Execution Record — `execution.json`

Records what was run, in an environment that may no longer exist.

| Field | Required | Description |
|---|---|---|
| `run_id` | yes | Identifier of the execution |
| `started_at` | yes | ISO 8601 timestamp |
| `finished_at` | yes | ISO 8601 timestamp |
| `code_version` | yes | Commit or tag |
| `config_version` | yes | Configuration file identifier or hash |
| `parameters` | yes | Runtime parameters |
| `dependencies` | yes | Name and version of each dependency that affects the result |
| `environment` | yes | OS, runtime version, relevant environment variables |
| `random_seed` | if applicable | The seed, or an explicit statement that none was used |
| `external_services` | if applicable | Service, version or response snapshot, and retrieval time |
| `outputs` | yes | Paths of produced files |
| `reproduction_command` | recommended | The exact command that reproduces the run |
| `reproducibility_limits` | recommended | What cannot be reproduced, and why |

#### Example

```json
{
  "run_id": "run-20261109-1420",
  "started_at": "2026-11-09T14:20:00+08:00",
  "finished_at": "2026-11-09T14:20:09+08:00",
  "code_version": "7c1f2a9",
  "config_version": "sha256:1d90c4...",
  "parameters": {"currency": "USD", "locale": "en-US", "batch": "batch-20261109-01"},
  "dependencies": {"python": "3.12.4", "requests": "2.32.3", "pandas": "2.2.2"},
  "environment": {"os": "linux-6.8", "cpu_arch": "x86_64"},
  "random_seed": null,
  "external_services": [
    {"service": "exchange-rate-api", "version": "v1", "snapshot": "data/raw/exchange_rates/2026-11-09.json"}
  ],
  "outputs": ["data/output/listings_report.json"],
  "reproduction_command": "python3 scripts/run_listings.py --batch batch-20261109-01",
  "reproducibility_limits": "External price API is queried live; the 2026-11-09 snapshot is used for exact reproduction."
}
```

### 2.5 Modification Record — `modification.json`

Records a change made to stored data.

| Field | Required | Description |
|---|---|---|
| `target` | yes | Path of the modified file |
| `previous_version` | yes | Path or identifier of the pre-modification version |
| `new_version` | yes | Path of the new version |
| `previous_sha256` | yes | Hash before |
| `new_sha256` | yes | Hash after |
| `reason` | yes | Why the change was necessary |
| `modified_by` | yes | Program or person that made the change |
| `modified_at` | yes | ISO 8601 timestamp |
| `reversible` | yes | Whether the previous version can restore the original |

### 2.6 Privacy Record — `privacy.json`

Records how sensitive content was handled.

| Field | Required | Description |
|---|---|---|
| `data_name` | yes | Which data the handling applies to |
| `fields_masked` | yes | Fields masked, and the masking method |
| `fields_retained` | yes | Fields kept in the clear, and why they are safe |
| `fields_not_persisted` | yes | Fields deliberately not written |
| `retention` | yes | How long the retained content is kept |
| `limitation` | if content was dropped | What could not be saved and what was recorded instead |

Masking one field never justifies deleting the audit records for the whole event. The event record is kept; the sensitive field is protected.

---

## 3. Relationship Between Records

```
source.json ──► raw/ ──► transform.json ──► processed/ ──► reconciliation.json
                    │                                               │
                    └──────────────► execution.json ◄───────────────┘
                                               │
                                               ▼
                                        output/ + audit/
```

- `source.json` describes the input to the first transformation.
- Each `transform.json` describes one step and references its input by hash.
- `reconciliation.json` spans the stages and closes the arithmetic.
- `execution.json` spans everything and describes the environment.
- `modification.json` attaches to any file that was changed after creation.
- `privacy.json` attaches to any dataset containing sensitive fields.

`run_id` links all records from one execution. `sha256` links records to the exact file content they describe.

---

## 4. Minimal Acceptable Set

When a task is small, the full set above is disproportionate. The minimum that still satisfies the standard:

| Situation | Required records |
|---|---|
| Read-only analysis of existing data | `source.json` for each input, `execution.json` |
| Processing that changes data | The above, plus one `transform.json` per stage and `reconciliation.json` |
| Data with sensitive fields | The above, plus `privacy.json` |
| Data corrected after collection | The above, plus `modification.json` |

An omission must be a deliberate choice, not an oversight. If a record was skipped, say which one and why.

---

## 5. Verification Checklist

Before claiming that data processing is auditable, confirm:

- [ ] Every input has a source record with a confirmed locator.
- [ ] Every raw file exists at the recorded path and still matches its hash.
- [ ] No raw file was edited after collection.
- [ ] Every transformation has a record naming its inputs, outputs, and rules.
- [ ] Counts reconcile at every stage, or the discrepancy is stated.
- [ ] Every excluded record has a counted reason.
- [ ] The execution record names a code version, dependencies, and a reproduction command.
- [ ] Known reproduction limits are stated.
- [ ] Sensitive fields are masked per the privacy record.
- [ ] A person who did not run the process can follow it from these records alone.

If any item cannot be confirmed, the processing is not fully auditable, and the report must say so.

---

## Related Documents

- [Data Audit and Reproducibility](../skills/data-audit-reproducibility/SKILL.md) — the standard these records satisfy.
- [Data First Execution](../skills/data-first-execution/SKILL.md) — when processing may be skipped entirely.
- [Engineering Principles](engineering-principles.md) — the principle behind preserving facts.
- [Terminology](terminology.md) — the vocabulary used above.
