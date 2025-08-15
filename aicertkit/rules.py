from __future__ import annotations
from typing import Dict, Any, Optional
from pathlib import Path

DEFAULT_RULES: Dict[str, Any] = {
    "version": "0.1.0",
    "categories": ["prohibited", "high_risk", "limited_risk", "minimal_risk", "gpai"],
    "obligations": [
        {"id":"RISK_MGMT","name":"Risk management process documented","applies_if":["high_risk|gpai"],"severity":"high"},
        {"id":"DATA_GOV","name":"Data governance + lineage documented","applies_if":["high_risk|gpai"],"severity":"high"},
        {"id":"TECH_DOC","name":"Technical documentation prepared","applies_if":["high_risk|gpai"],"severity":"high"},
        {"id":"RECORDS","name":"Logging & traceability implemented","applies_if":["high_risk"],"severity":"medium"},
        {"id":"TRANSPARENCY","name":"User transparency & labeling of AI output","applies_if":["high_risk","limited_risk","gpai"],"severity":"medium"},
        {"id":"HUMAN_OVERSIGHT","name":"Human oversight defined","applies_if":["high_risk"],"severity":"high"},
        {"id":"ACCURACY","name":"Accuracy metrics & evaluation documented","applies_if":["high_risk|gpai"],"severity":"high"},
        {"id":"ROBUSTNESS","name":"Robustness & cybersecurity controls","applies_if":["high_risk|gpai"],"severity":"high"},
        {"id":"POST_MARKET","name":"Post-market monitoring plan","applies_if":["high_risk"],"severity":"medium"},
        {"id":"TRAIN_DATA_SUM","name":"Training data summary for GPAI","applies_if":["gpai"],"severity":"medium"},
        {"id":"SYSTEMIC_RISK","name":"Systemic risk assessment (if applicable)","applies_if":["gpai"],"severity":"high"}
    ]
}

def load_rules(path: Optional[Path]) -> Dict[str, Any]:
    # For MVP: ignore file parsing and just return embedded defaults
    return DEFAULT_RULES
