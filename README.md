# ML Experiment Reproducibility Agent

A local, read-only audit tool for identifying missing metadata and recorded environment differences that can make ML experiments difficult to reproduce.

## Features
- Checks required experiment manifest fields.
- Compares selected environment fields against a reference record.
- Checks expected artifact names against a supplied inventory.
- Writes a JSON report with rule IDs, severity, evidence, and limitations.
- Uses Python's standard library only.

## Quick start
```bash
python -m unittest discover -s tests -v
python verification/readiness_audit.py
python -m core.cli examples/experiment.json --reference-environment examples/reference_environment.json --artifact-inventory examples/artifact_inventory.json --output reproducibility-report.json
```

An audit status of `issues_found` is not necessarily a tool failure: it means the input records contain reproducibility gaps or mismatches.

## Manifest format
Required top-level fields: `experiment_id`, `code_revision`, `dataset`, `random_seed`, `parameters`, `environment`, `metrics`, and `expected_artifacts`. See `examples/experiment.json`.

## Scope
The tool does not launch experiments, install dependencies, connect to registries, or modify supplied artifacts. A clean report is not proof of bitwise reproducibility or scientific validity.
