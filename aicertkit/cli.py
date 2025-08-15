from __future__ import annotations
import argparse, sys
from pathlib import Path
from .scanner import scan_repo, render_bundle

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="aicertkit", description="Scan a repo & output an AI-Act–ready Compliance Bundle")
    sub = p.add_subparsers(dest="cmd", required=True)
    sc = sub.add_parser("scan", help="Scan a repository and write the Compliance Bundle")
    sc.add_argument("repo", type=str, help="Path to the repository to scan")
    sc.add_argument("-o", "--out", type=str, default=None, help="Output directory for the bundle")
    sc.add_argument("--rules", type=str, default=None, help="Path to ai_act_rules.yaml (optional)")
    return p

def run_scan(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    if not repo.exists() or not repo.is_dir():
        print(f"[!] repo path not found: {repo}", file=sys.stderr)
        return 2
    out_dir = Path(args.out) if args.out else repo / "compliance_bundle"
    rules_path = Path(args.rules).resolve() if args.rules else None
    report = scan_repo(repo, rules_path)
    paths = render_bundle(report, out_dir)
    print("[+] Compliance Bundle written:")
    for name, path in paths.items():
        print(f"    - {name}: {path}")
    return 0

def main(argv=None) -> int:
    p = build_parser()
    args = p.parse_args(argv)
    if args.cmd == "scan":
        return run_scan(args)
    return 0
if __name__ == "__main__":
    import sys
    raise SystemExit(main())
