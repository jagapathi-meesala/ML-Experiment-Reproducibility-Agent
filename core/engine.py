"""Deterministic, read-only reproducibility metadata audit."""
from __future__ import annotations

REQUIRED_FIELDS = (
    "experiment_id", "code_revision", "dataset", "random_seed",
    "parameters", "environment", "metrics", "expected_artifacts",
)
ENVIRONMENT_FIELDS = ("python_version", "framework", "framework_version", "accelerator")
LIMITATIONS = [
    "The audit checks supplied metadata and inventory records only.",
    "It does not execute training or verify dataset contents, code availability, or artifact bytes.",
    "A clean report does not guarantee bitwise or scientific reproducibility.",
]

def _finding(rule_id, severity, message, evidence=None):
    return {"rule_id": rule_id, "severity": severity, "message": message, "evidence": evidence or {}}

def audit_manifest(manifest):
    findings = []
    if not isinstance(manifest, dict):
        return {"status": "invalid_input", "findings": [_finding("MAN-000", "error", "Manifest must be a JSON object.")], "summary": {"errors": 1, "warnings": 0, "info": 0}, "limitations": LIMITATIONS}
    for field in REQUIRED_FIELDS:
        if field not in manifest:
            findings.append(_finding("MAN-001", "error", f"Required field is missing: {field}", {"field": field}))
    if "experiment_id" in manifest and (not isinstance(manifest["experiment_id"], str) or not manifest["experiment_id"].strip()):
        findings.append(_finding("MAN-002", "error", "experiment_id must be a non-empty string.", {"field": "experiment_id"}))
    if "code_revision" in manifest and (not isinstance(manifest["code_revision"], str) or not manifest["code_revision"].strip()):
        findings.append(_finding("MAN-003", "error", "code_revision must be a non-empty string.", {"field": "code_revision"}))
    dataset = manifest.get("dataset")
    if "dataset" in manifest and (not isinstance(dataset, dict) or not isinstance(dataset.get("identifier"), str) or not dataset.get("identifier", "").strip()):
        findings.append(_finding("MAN-004", "error", "dataset.identifier must be recorded as a non-empty string.", {"field": "dataset.identifier"}))
    if "random_seed" in manifest and manifest["random_seed"] is not None and (not isinstance(manifest["random_seed"], int) or isinstance(manifest["random_seed"], bool)):
        findings.append(_finding("MAN-005", "error", "random_seed must be an integer or null when explicitly unknown.", {"field": "random_seed"}))
    for field in ("parameters", "environment", "metrics"):
        if field in manifest and not isinstance(manifest[field], dict):
            findings.append(_finding("MAN-006", "error", f"{field} must be a JSON object.", {"field": field}))
    if "expected_artifacts" in manifest and (not isinstance(manifest["expected_artifacts"], list) or any(not isinstance(x, str) or not x.strip() for x in manifest["expected_artifacts"])):
        findings.append(_finding("MAN-007", "error", "expected_artifacts must be a list of non-empty strings.", {"field": "expected_artifacts"}))
    if manifest.get("random_seed") is None and "random_seed" in manifest:
        findings.append(_finding("MAN-008", "warning", "Random seed is explicitly unknown; stochastic behavior may be harder to reproduce.", {"field": "random_seed"}))
    if not manifest.get("metrics"):
        findings.append(_finding("MAN-009", "warning", "No metrics are recorded in the manifest.", {"field": "metrics"}))
    if not manifest.get("parameters"):
        findings.append(_finding("MAN-010", "warning", "No experiment parameters are recorded.", {"field": "parameters"}))
    return _report(findings)

def compare_environment(environment, reference, fields=ENVIRONMENT_FIELDS):
    findings = []
    if not isinstance(environment, dict) or not isinstance(reference, dict):
        findings.append(_finding("ENV-000", "error", "Both environment records must be JSON objects."))
        return _report(findings)
    for field in fields:
        if field not in environment or field not in reference:
            findings.append(_finding("ENV-001", "info", f"Comparison skipped; field absent from one or both records: {field}", {"field": field}))
        elif environment[field] != reference[field]:
            findings.append(_finding("ENV-002", "warning", f"Recorded environment differs for {field}.", {"field": field, "experiment_value": environment[field], "reference_value": reference[field]}))
    return _report(findings)

def check_artifacts(expected, inventory):
    findings = []
    if not isinstance(expected, list) or not isinstance(inventory, list):
        return _report([_finding("ART-000", "error", "Expected artifacts and inventory must both be lists.")])
    present = {x for x in inventory if isinstance(x, str)}
    for artifact in expected:
        if artifact not in present:
            findings.append(_finding("ART-001", "warning", f"Expected artifact is not listed in the supplied inventory: {artifact}", {"artifact": artifact}))
    if not findings:
        findings.append(_finding("ART-002", "info", "All expected artifact names are listed in the supplied inventory."))
    return _report(findings)

def _report(findings):
    summary = {level + "s": sum(1 for f in findings if f["severity"] == level) for level in ("error", "warning", "info")}
    status = "error" if summary["errors"] else ("issues_found" if summary["warnings"] else "passed")
    return {"status": status, "findings": findings, "summary": summary, "limitations": LIMITATIONS}
