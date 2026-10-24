"""Command-line interface for local experiment reproducibility audits."""
import argparse
import json
from pathlib import Path
from core.engine import audit_manifest, compare_environment, check_artifacts, LIMITATIONS

def _load(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)

def run_audit(manifest, reference_environment=None, artifact_inventory=None):
    report = audit_manifest(manifest)
    findings = list(report["findings"])
    if reference_environment is not None:
        env_report = compare_environment(manifest.get("environment", {}), reference_environment)
        findings.extend(env_report["findings"])
    if artifact_inventory is not None:
        art_report = check_artifacts(manifest.get("expected_artifacts", []), artifact_inventory)
        findings.extend(art_report["findings"])
    summary = {level + "s": sum(1 for f in findings if f["severity"] == level) for level in ("error", "warning", "info")}
    status = "error" if summary["errors"] else ("issues_found" if summary["warnings"] else "passed")
    return {"agent": "ML Experiment Reproducibility Agent", "status": status, "experiment_id": manifest.get("experiment_id") if isinstance(manifest, dict) else None, "summary": summary, "findings": findings, "limitations": LIMITATIONS}

def main():
    parser = argparse.ArgumentParser(description="Audit ML experiment reproducibility metadata.")
    parser.add_argument("manifest", help="Path to experiment manifest JSON")
    parser.add_argument("--reference-environment", help="Optional reference environment JSON")
    parser.add_argument("--artifact-inventory", help="Optional artifact inventory JSON")
    parser.add_argument("--output", default="reproducibility-report.json", help="Output JSON report path")
    args = parser.parse_args()
    manifest = _load(args.manifest)
    reference = _load(args.reference_environment) if args.reference_environment else None
    inventory_doc = _load(args.artifact_inventory) if args.artifact_inventory else None
    inventory = inventory_doc.get("artifacts", []) if isinstance(inventory_doc, dict) else inventory_doc
    report = run_audit(manifest, reference, inventory)
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "summary": report["summary"], "output": args.output}, indent=2))
    return 1 if report["status"] == "error" else 0

if __name__ == "__main__":
    raise SystemExit(main())
