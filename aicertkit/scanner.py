from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple
from datetime import datetime

from .utils import walk_files, read_text_safe, file_sha256
from .rules import load_rules
from .renderers import render_model_card, render_data_card, render_risk_yaml

LLM_TERMS = [
    "transformers", "langchain", "openai", "anthropic", "gpt-", "llama", "mistral",
    "vllm", "llama.cpp", "llm", "rag", "prompt", "chain of thought"
]
SENSITIVE_TERMS = [
    "biometric", "employment", "recruit", "credit scoring", "lending", "admission",
    "education", "medical diagnosis", "critical infrastructure", "law enforcement",
    "border control", "facial recognition", "social scoring"
]

def scan_repo(repo_path: Path, rules_path: Path|None = None) -> Dict[str, Any]:
    repo_path = repo_path.resolve()
    rules = load_rules(rules_path)
    files = list(walk_files(repo_path))
    meta = _collect_metadata(repo_path, files)
    detections = _detect_signals(repo_path, files)
    triage = _ai_act_triage(detections, rules)
    owasp = _owasp_llm_evaluate(detections)
    return {
        "metadata": meta,
        "detections": detections,
        "ai_act": triage,
        "owasp_llm": owasp,
        "generated": datetime.utcnow().isoformat() + "Z"
    }

def _collect_metadata(root: Path, files: List[Path]) -> Dict[str, Any]:
    size_total = sum(p.stat().st_size for p in files) if files else 0
    return {
        "repo_name": root.name,
        "files_count": len(files),
        "bytes": size_total,
        "has_readme": (root / "README.md").exists(),
        "hash_sample": file_sha256(files[0]) if files else None
    }

def _detect_signals(root: Path, files: List[Path]) -> Dict[str, Any]:
    llm_hits: List[Tuple[str,str]] = []
    sensitive_hits: List[Tuple[str,str]] = []
    data_files = []
    for p in files:
        rel = str(p.relative_to(root))
        if any(rel.lower().endswith(ext) for ext in [".csv",".json",".parquet",".tsv",".xlsx"]):
            data_files.append(rel)
        text = ""
        if p.suffix.lower() in [".py",".md",".txt",".toml",".json",".yaml",".yml",".js",".ts"]:
            text = read_text_safe(p).lower()
        if text:
            for term in LLM_TERMS:
                if term in text: llm_hits.append((rel, term))
            for term in SENSITIVE_TERMS:
                if term in text: sensitive_hits.append((rel, term))
    return {
        "llm_detected": bool(llm_hits),
        "llm_hits": llm_hits[:50],
        "sensitive_hits": sensitive_hits[:50],
        "data_files": data_files[:100],
        "license_present": (root / "LICENSE").exists()
    }

def _ai_act_triage(detections: Dict[str, Any], rules: Dict[str, Any]) -> Dict[str, Any]:
    if any("social scoring" in s for _, s in detections.get("sensitive_hits", [])):
        risk = "prohibited"
    elif detections.get("sensitive_hits"):
        risk = "high_risk"
    elif detections.get("llm_detected"):
        risk = "gpai"
    else:
        risk = "minimal_risk"

    obligations = []
    for ob in rules.get("obligations", []):
        applies = any(
            (c == "gpai" and risk=="gpai") or
            (c == "high_risk" and risk=="high_risk") or
            (c == "limited_risk" and risk=="limited_risk")
            for cond in ob.get("applies_if", []) for c in cond.split("|")
        )
        obligations.append({
            "id": ob.get("id"),
            "name": ob.get("name"),
            "severity": ob.get("severity","medium"),
            "applies": applies,
            "status": "todo" if applies else "n/a"
        })
    return {"rules_version": rules.get("version","0"), "risk_level": risk, "obligations": obligations}

def _owasp_llm_evaluate(detections: Dict[str, Any]) -> Dict[str, Any]:
    top10 = [
        ("LLM01", "Prompt Injection"), ("LLM02", "Insecure Output Handling"),
        ("LLM03", "Training Data Poisoning"), ("LLM04", "Model Denial of Service"),
        ("LLM05", "Supply Chain Vulnerabilities"), ("LLM06", "Sensitive Information Disclosure"),
        ("LLM07", "Insecure Plugin/Tool Design"), ("LLM08", "Excessive Agency"),
        ("LLM09", "Overreliance"), ("LLM10","Model Theft")
    ]
    llm = detections.get("llm_detected", False)
    results = []
    for cid, name in top10:
        applicable = llm
        status = "warn" if applicable else "n/a"
        evidence = detections.get("llm_hits", []) if applicable else []
        if cid == "LLM06" and detections.get("sensitive_hits"):
            status = "fail"; evidence = detections["sensitive_hits"]
        results.append({"id": cid, "name": name, "applicable": applicable, "status": status, "evidence": evidence[:10]})
    return {"checks": results}

def render_bundle(report: Dict[str, Any], out_dir: Path) -> Dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    meta = report["metadata"]; ai = report["ai_act"]; det = report["detections"]; gen = report["generated"]
    mc_ctx = {
        "repo_name": meta["repo_name"], "version": "0.1.0", "generated": gen,
        "training_data_summary": ", ".join(det.get("data_files", [])[:10]) or "None",
        "risk_level": ai["risk_level"]
    }
    dc_ctx = {"repo_name": meta["repo_name"], "generated": gen}
    risk_doc = {"generated": gen, "repo": meta["repo_name"], "risk_level": ai["risk_level"], "obligations": ai["obligations"]}
    paths = {}
    (out_dir/"model_card.md").write_text(render_model_card(mc_ctx), encoding="utf-8"); paths["model_card.md"] = out_dir/"model_card.md"
    (out_dir/"data_card.md").write_text(render_data_card(dc_ctx), encoding="utf-8"); paths["data_card.md"] = out_dir/"data_card.md"
    (out_dir/"risk.yaml").write_text(render_risk_yaml(risk_doc), encoding="utf-8"); paths["risk.yaml"] = out_dir/"risk.yaml"
    (out_dir/"owasp_llm_checks.json").write_text(json.dumps(report["owasp_llm"], indent=2), encoding="utf-8"); paths["owasp_llm_checks.json"] = out_dir/"owasp_llm_checks.json"
    return paths
