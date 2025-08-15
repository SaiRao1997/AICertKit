
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime
from .rules import load_rules
from .renderers import render_model_card, render_data_card, render_risk_yaml

def scan_repo(repo_path: Path, rules_path: Path|None = None):
    repo_path = repo_path.resolve()
    rules = load_rules(rules_path)
    detections = {"llm_detected": True, "llm_hits": [("README.md","transformers")], "sensitive_hits": []}
    report = {
        "metadata": {"repo_name": repo_path.name},
        "detections": detections,
        "ai_act": {"rules_version": rules.get("version","0.0"), "risk_level": "gpai", "obligations": rules["obligations"]},
        "owasp_llm": {"checks":[{"id":"LLM01","name":"Prompt Injection","applicable":True,"status":"warn","evidence":[]}] + [{"id":f"LLM0{i}","name":"","applicable":True,"status":"warn","evidence":[]} for i in range(2,10)] + [{"id":"LLM10","name":"","applicable":True,"status":"warn","evidence":[]}],
        "generated": datetime.utcnow().isoformat() + "Z"
    }
    return report

def render_bundle(report, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    mc = render_model_card({"repo_name": report["metadata"]["repo_name"], "generated": report["generated"]})
    dc = render_data_card({"repo_name": report["metadata"]["repo_name"], "generated": report["generated"]})
    risk = render_risk_yaml({"generated": report["generated"], "repo": report["metadata"]["repo_name"]})
    (out_dir/"model_card.md").write_text(mc, encoding="utf-8")
    (out_dir/"data_card.md").write_text(dc, encoding="utf-8")
    (out_dir/"risk.yaml").write_text(risk, encoding="utf-8")
    (out_dir/"owasp_llm_checks.json").write_text(json.dumps(report["owasp_llm"], indent=2), encoding="utf-8")
    return out_dir
