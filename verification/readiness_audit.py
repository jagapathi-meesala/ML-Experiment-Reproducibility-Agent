from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    "agent.yaml", "SOUL.md", "AGENTS.md", "RULES.md", "DUTIES.md",
    "EXPLAINABILITY.md", "README.md", "requirements.txt", "config/default.yaml",
    "contracts/experiment-manifest.schema.json", "core/engine.py", "core/cli.py",
    "tools/experiment_manifest_audit.yaml", "tools/environment_drift_check.yaml",
    "tools/reproducibility_report.yaml", "skills/experiment-manifest-audit/SKILL.md",
    "skills/environment-drift-check/SKILL.md", "skills/reproducibility-report/SKILL.md",
    "examples/experiment.json", "tests/test_engine.py"
]
missing = [p for p in required if not (ROOT / p).is_file()]
manifest_text = (ROOT / "agent.yaml").read_text()
name_match = re.search(r'^name:\s*"([^"]+)"', manifest_text, re.MULTILINE)
tools_count = len(re.findall(r"^  - ", manifest_text.split("skills:")[0], re.MULTILINE))
skills_text = manifest_text.split("skills:", 1)[1] if "skills:" in manifest_text else ""
skills_count = len(re.findall(r"^  - ", skills_text, re.MULTILINE))
explain = (ROOT / "EXPLAINABILITY.md").read_text()
expected_headings = ["## Decision", "## Inputs", "## Limits"]
print(f"Required files: {len(required)-len(missing)}/{len(required)}")
print(f"Agent name: {name_match.group(1) if name_match else 'MISSING'}")
print(f"Tools: {tools_count}; skills: {skills_count}")
print(f"Explainability headings: {'PASS' if all(h in explain for h in expected_headings) else 'FAIL'}")
if missing:
    print("Missing:", ", ".join(missing))
if missing or 'schema_version: "0.1.0"' not in manifest_text or not name_match or not all(h in explain for h in expected_headings):
    sys.exit(1)
print("Readiness audit: PASS (local structural checks only; not OpenGAP/HiDevs validation)")
