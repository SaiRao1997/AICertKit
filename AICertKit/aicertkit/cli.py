
from __future__ import annotations
import argparse, sys
from pathlib import Path
from .scanner import scan_repo, render_bundle

def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("cmd")
    p.add_argument("repo")
    p.add_argument("-o","--out", default=None)
    args = p.parse_args(argv)
    if args.cmd == "scan":
        repo = Path(args.repo)
        out_dir = Path(args.out) if args.out else repo / "compliance_bundle"
        report = scan_repo(repo, None)
        render_bundle(report, out_dir)
        print(str(out_dir))
        return 0
    return 2
