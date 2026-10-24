# Explainability

## Decision
The agent evaluates experiment metadata using explicit required-field, environment-comparison, and artifact-inventory rules. Each finding includes a stable rule ID, severity, and evidence.

## Inputs
The agent accepts a JSON experiment manifest, an optional JSON reference environment, and an optional JSON artifact inventory. The manifest records the run identifier, code revision, dataset reference, seed, configuration, environment, and expected artifacts.

## Limits
The audit checks only the supplied records. It does not execute training, validate dataset contents, prove a code revision is available, verify artifact bytes, or guarantee exact or scientific reproducibility. Environment differences are reported only for configured fields present in both records.
