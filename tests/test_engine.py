import unittest
from core.engine import audit_manifest, compare_environment, check_artifacts
from core.cli import run_audit

def valid_manifest():
    return {
        "experiment_id": "run-1", "code_revision": "abc123",
        "dataset": {"identifier": "dataset-v1"}, "random_seed": 7,
        "parameters": {"lr": 0.01}, "environment": {"python_version": "3.11", "framework": "torch", "framework_version": "2.0", "accelerator": "CPU"},
        "metrics": {"accuracy": 0.9}, "expected_artifacts": ["model.pt"]
    }

class TestEngine(unittest.TestCase):
    def test_valid_manifest_passes(self):
        self.assertEqual(audit_manifest(valid_manifest())["status"], "passed")
    def test_missing_required_field_is_error(self):
        manifest = valid_manifest()
        del manifest["code_revision"]
        self.assertEqual(audit_manifest(manifest)["status"], "error")
    def test_environment_drift_reported(self):
        result = compare_environment({"framework_version": "2.0"}, {"framework_version": "2.1"})
        self.assertTrue(any(f["rule_id"] == "ENV-002" for f in result["findings"]))
    def test_missing_artifact_reported(self):
        result = check_artifacts(["model.pt", "metrics.json"], ["model.pt"])
        self.assertTrue(any(f["rule_id"] == "ART-001" for f in result["findings"]))
    def test_combined_audit(self):
        result = run_audit(valid_manifest(), {"framework_version": "2.1"}, ["model.pt"])
        self.assertEqual(result["status"], "issues_found")
        self.assertGreaterEqual(result["summary"]["warnings"], 1)

if __name__ == "__main__":
    unittest.main()
