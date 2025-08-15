# AICertKit

AICertKit scans a code repository and produces a starter **Compliance Bundle** you can use in reviews or CI:

- `risk.yaml` — EU AI Act risk triage + obligations checklist (heuristic)
- `model_card.md` — draft model card (fill in details)
- `data_card.md` — draft data card (fill in details)
- `owasp_llm_checks.json` — baseline OWASP LLM Top‑10 results

> This is scaffolding for engineers, not legal advice.

---

## What it does (plain English)

- Detects LLM usage signals (e.g., `transformers`, `openai`, `llama`, `rag`).
- Looks for sensitive/high‑risk hints (employment, biometrics, etc.).
- Assigns a coarse risk level: `prohibited`, `high_risk`, `gpai`, or `minimal_risk`.
- Writes the four files above into the output folder you choose.

---

## Quick start (local)

> Use a virtual environment so nothing touches your system Python. You can delete the folder later.

### Windows (PowerShell)

```powershell
git clone https://github.com/SaiRao1997/AICertKit.git
cd AICertKit

py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m aicertkit.cli scan .ixtures\sample_repo -o .\outundle
dir .\outundle
```

### macOS / Linux

```bash
git clone https://github.com/SaiRao1997/AICertKit.git
cd AICertKit

python -m venv .venv
source .venv/bin/activate

python -m aicertkit.cli scan ./fixtures/sample_repo -o ./out/bundle
ls ./out/bundle
```

**Run on any local repo** (change the path and output folder):

```bash
python -m aicertkit.cli scan /path/to/your/repo -o ./out/your_repo_bundle
```

Expected output folder contents:

```
out/<your_repo_bundle>/
├─ risk.yaml
├─ model_card.md
├─ data_card.md
└─ owasp_llm_checks.json
```

---

## Use in GitHub Actions (PR artifact)

Create `.github/workflows/compliance-bundle.yml` in the repo you want to scan:

```yaml
name: Compliance Bundle
on:
  pull_request:
  workflow_dispatch:

jobs:
  bundle:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install "git+https://github.com/SaiRao1997/AICertKit.git#egg=aicertkit"
      - run: aicertkit scan . -o compliance_bundle || python -m aicertkit.cli scan . -o compliance_bundle
      - uses: actions/upload-artifact@v4
        with:
          name: compliance_bundle
          path: compliance_bundle
```

> Tip: To block merges when risk is `prohibited`, add a step that loads `compliance_bundle/risk.yaml` and exits non‑zero if it equals `prohibited`.

---

## Customize (optional)

- **Rules / obligations:** edit `aicertkit/rules.py`.
- **Signals / keywords:** edit `LLM_TERMS` and `SENSITIVE_TERMS` in `aicertkit/scanner.py`.
- **Card templates:** edit `aicertkit/renderers.py`.

---

## Troubleshooting

- **“No module named aicertkit”** — run from repo root and use the venv:
  ```bash
  python -m aicertkit.cli scan ./fixtures/sample_repo -o ./out/bundle
  ```
- **Windows venv won’t activate** — in PowerShell:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```
- **Accidentally committed outputs** — add to `.gitignore` and recommit:
  ```
  .venv/
  __pycache__/
  out/
  .pytest_cache/
  *.egg-info/
  ```

---

## License

MIT © AICertKit Maintainers
