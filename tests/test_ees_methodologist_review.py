import importlib.util
import json
from pathlib import Path


def load_module():
    script_path = Path(__file__).resolve().parents[1] / "simulation.py"
    spec = importlib.util.spec_from_file_location("ees_methodologist_review_simulation", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_main_writes_relative_report(tmp_path):
    module = load_module()

    projects_root = tmp_path / "projects"
    upstream_dir = projects_root / "exascale-evidence-singularity"
    upstream_dir.mkdir(parents=True)
    (upstream_dir / "certification.json").write_text(json.dumps({"status": "OMEGA"}), encoding="utf-8")

    report_root = tmp_path / "report"
    report_root.mkdir()

    result = module.main(project_root=report_root, projects_root=projects_root)

    report_path = report_root / "omega_audit_report.json"
    assert report_path.exists()
    assert result["status"] == "OMEGA_POINT_CERTIFIED"
    assert len(result["final_dialogue"]) == 4
    assert all("pending" not in line.lower() for line in result["final_dialogue"])
