#!/usr/bin/env python3
"""
Read the ops log back and summarise it — UNIT 9.

    python summarize_log.py                      # logs/requests.jsonl
    python summarize_log.py path/to/other.jsonl
    python summarize_log.py --since 2026-11-08T06:00   # only lines at/after this UTC time

It answers questions from the log alone, without touching the service:
how many requests, what came back, how long /submit took (cold and warm
separately), where the time went, and what a request cost in CPU.

Standard library only.
"""

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

import config

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass


def load(path: Path, since: str | None = None) -> list[dict]:
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if since and e.get("ts", "") < since:
            continue
        entries.append(e)
    return entries


def percentile(values: list[float], p: float) -> float:
    """Nearest-rank percentile. Fine for the sample sizes used here."""
    if not values:
        return float("nan")
    s = sorted(values)
    rank = math.ceil(p / 100 * len(s))
    return s[max(0, min(len(s) - 1, rank - 1))]


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else float("nan")


def latency_line(label: str, values: list[float]) -> str:
    if not values:
        return f"  {label:<22} n=0"
    return (
        f"  {label:<22} n={len(values):<4} "
        f"mean={mean(values):8.1f}  p50={percentile(values, 50):8.1f}  "
        f"p95={percentile(values, 95):8.1f}  max={max(values):8.1f}  (ms)"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Summarise the ops log.")
    ap.add_argument("path", nargs="?", default=str(config.OPS_LOG))
    ap.add_argument("--since", help="ISO timestamp (UTC); ignore earlier lines")
    args = ap.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"No ops log at {path}")
        return 1
    entries = load(path, args.since)
    if not entries:
        print("No entries.")
        return 1

    print(f"{len(entries)} requests   {entries[0]['ts']}  ->  {entries[-1]['ts']}")

    print("\nBy route and status:")
    by = Counter((e["route"], e["status"]) for e in entries)
    for (route, status), n in sorted(by.items()):
        print(f"  {route:<10} {status}  x{n}")

    server_errors = sum(1 for e in entries if e["status"] >= 500)
    rejected = sum(1 for e in entries if e["status"] in (413, 422, 429))
    print(f"\n5xx (service failures): {server_errors} of {len(entries)}"
          f"   rejected (413/422/429): {rejected}")

    submits = [e for e in entries if e["route"] == "/submit" and e["status"] == 200]
    cold = [e for e in submits if e.get("model_cold")]
    warm = [e for e in submits if e.get("model_cold") is False]

    print("\n/submit 200 latency:")
    print(latency_line("cold (model load)", [e["duration_ms"] for e in cold]))
    print(latency_line("warm", [e["duration_ms"] for e in warm]))

    print("\nWhere the time goes, warm /submit 200 (mean ms per stage):")
    if warm:
        total = mean([e["duration_ms"] for e in warm])
        for stage in ("gpt2", "style", "scoring", "audit"):
            vals = [e["stage_ms"].get(stage, 0.0) for e in warm if e.get("stage_ms")]
            if vals:
                share = 100 * mean(vals) / total if total else float("nan")
                print(f"  {stage:<8} {mean(vals):8.2f}  ({share:5.1f}% of request)")
    else:
        print("  no warm requests")

    print("\nCPU per /submit 200 (cpu_ms; only meaningful for serial runs):")
    for label, group in (("cold", cold), ("warm", warm)):
        vals = [e["cpu_ms"] for e in group if e.get("cpu_ms") is not None]
        if vals:
            print(f"  {label:<6} n={len(vals):<4} mean={mean(vals):8.1f} ms"
                  f"   total={sum(vals) / 1000:.2f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
