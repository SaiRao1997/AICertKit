from __future__ import annotations
from typing import Dict, Any

def render_model_card(ctx: Dict[str, Any]) -> str:
    return f"""# Model Card: {ctx['repo_name']}

**Version:** {ctx['version']}
**Generated:** {ctx['generated']}

## Overview
Auto-generated draft based on repository scan.

## Intended Use
To be filled by maintainers.

## Data Summary
Detected data files (heuristic): {ctx['training_data_summary']}

## Evaluation
- Metrics: N/A
- Test data: N/A

## Risks & Limitations
Initial risk level (heuristic): {ctx['risk_level']}
This card is a starting point; complete it with project-specific details.

## Ethical Considerations
Consider fairness, bias, and potential misuse.

## Security & Robustness
Document robustness, adversarial testing, and monitoring.

## Human Oversight
Describe human-in-the-loop mechanisms if any.
"""

def render_data_card(ctx: Dict[str, Any]) -> str:
    return f"""# Data Card: {ctx['repo_name']}

**Generated:** {ctx['generated']}

## Dataset Overview
Dataset(s) referenced in the repository (detected heuristically).

## Collection & Provenance
Describe data sources and consent/collection processes.

## Preprocessing
List cleaning, filtering, augmentation steps.

## Licensing & Usage
Specify dataset licenses and any restrictions.

## PII & Privacy
Document PII handling, anonymization, retention, deletion.

## Bias & Representativeness
Describe sampling and representativeness considerations.

## Quality & Validation
Mention validation, labeling QA, and known issues.

## Governance
Roles, approvals, change management, and access control.
"""

def _yaml_escape(s: str) -> str:
    if any(c in s for c in ':#-{}[],&*?|>%@!\n\r\t'):
        return '"' + s.replace('"','\\"') + '"'
    return s

def render_risk_yaml(risk: Dict[str, Any]) -> str:
    lines = []
    lines.append(f"generated: {_yaml_escape(risk['generated'])}")
    lines.append(f"repo: {_yaml_escape(risk['repo'])}")
    lines.append(f"risk_level: {_yaml_escape(risk['risk_level'])}")
    lines.append("obligations:")
    for ob in risk["obligations"]:
        lines.append("  - id: " + _yaml_escape(str(ob.get('id', ''))))
        lines.append("    name: " + _yaml_escape(str(ob.get('name', ''))))
        lines.append("    severity: " + _yaml_escape(str(ob.get('severity', ''))))
        lines.append("    applies: " + ("true" if ob.get('applies') else "false"))
        lines.append("    status: " + _yaml_escape(str(ob.get('status', ''))))
    lines.append('notes: "Heuristic triage. Review with your compliance team."')
    return "\n".join(lines) + "\n"
