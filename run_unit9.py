#!/usr/bin/env python3
"""
Unit 9 driver: runs the five criteria in criteria.md and records what happened.

    python run_unit9.py --check          # verify setup only; sends no requests
    python run_unit9.py --criterion 1    # one criterion (2 and 3 run together)
    python run_unit9.py                  # all five

It writes raw measurements to results/unit9_runs/unit9_run_<timestamp>.json and
prints one line per trial. For each trial it compares the measurements with the
target written in criteria.md and says "meets target", "misses target" or
"invalid". It does not write the diagnosis; that comes after reading the results.

Every trial that touches the model starts the real server with `python serve.py`
(the documented command), from this repo, on the default port.
"""

import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import config  # noqa: E402
import scenarios  # noqa: E402

BASE = f"http://127.0.0.1:{config.PORT}"
RUNS_DIR = ROOT / "results" / "unit9_runs"
ENV_FILE = ROOT / "results" / "unit8_environment.txt"
REF_FILE = ROOT / "results" / "unit8_reference_scores.json"

REQUIRED_FIELDS = ["ts", "request_id", "route", "status", "outcome", "duration_ms", "cpu_ms"]
ENV_KEYS = ("python", "gpt2_revision", "torch", "transformers")


# ── helpers ──────────────────────────────────────────────────────────────────

def scenario_texts(name):
    for sc in scenarios.SCENARIOS:
        if sc["name"] == name:
            return sc["texts"]
    raise KeyError(f"no scenario named {name!r}")


OWN = scenario_texts("my own writing")          # indices 1..10 in criteria, OWN[0..9]
WARM_INDICES = [1, 3, 4, 5, 6, 7, 8, 9, 10]     # criterion 3
WARM_TEXTS = [OWN[i - 1] for i in WARM_INDICES]
BATCH_TEXTS = OWN[:9]                           # criterion 1 200s use indices 1-9
LOAD_TEXTS = OWN[:10]                           # criterion 4 uses indices 1-10


def p95(values):
    """Nearest-rank p95: the value at rank ceil(0.95 * n), using integer maths."""
    s = sorted(values)
    rank = (95 * len(s) + 99) // 100
    return s[rank - 1]


def log_lines():
    path = config.OPS_LOG
    if not path.exists():
        return []
    return [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def submit(text, creator_id, timeout=60):
    t = time.perf_counter()
    try:
        r = requests.post(f"{BASE}/submit", json={"text": text, "creator_id": creator_id}, timeout=timeout)
    except requests.Timeout:
        return {"status": None, "timeout": True, "elapsed_s": time.perf_counter() - t,
                "request_id": None, "body": None}
    elapsed = time.perf_counter() - t
    try:
        body = r.json()
    except ValueError:
        body = None
    return {"status": r.status_code, "timeout": False, "elapsed_s": elapsed,
            "request_id": r.headers.get("X-Request-ID"), "body": body}


class Server:
    """Runs `python serve.py` with default settings, and stops it afterwards."""

    def __init__(self, label):
        self.label = label
        self.proc = None
        self._log = None

    def start(self):
        RUNS_DIR.mkdir(parents=True, exist_ok=True)
        env = {k: v for k, v in os.environ.items()
               if k not in ("AI201_RATE_LIMITS", "AI201_OPS_LOG", "AI201_THREADS", "HOST", "PORT")}
        self._log = open(RUNS_DIR / f"server_{self.label}.log", "w", encoding="utf-8")
        self.proc = subprocess.Popen([sys.executable, "serve.py"], cwd=ROOT, env=env,
                                     stdout=self._log, stderr=subprocess.STDOUT)
        deadline = time.time() + 60
        while time.time() < deadline:
            try:
                if requests.get(f"{BASE}/health", timeout=2).status_code == 200:
                    return
            except requests.RequestException:
                pass
            time.sleep(0.5)
        self.stop()
        raise RuntimeError(f"server {self.label} did not come up within 60 s")

    def stop(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(15)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait()
        if self._log:
            self._log.close()
        self.proc = None


# ── criterion 1: operational log completeness ────────────────────────────────

def crit1_trial(trial):
    limited = f"log-test-limited-{trial}"
    plan = []
    plan += [("limited", BATCH_TEXTS[k % 9], limited) for k in range(9)]
    plan += [("ok", BATCH_TEXTS[k % 9], f"c1-t{trial}-ok{k}") for k in range(6)]
    plan += [("422", "", f"c1-t{trial}-bad{k}") for k in range(3)]
    plan += [("413", "x" * 10001, f"c1-t{trial}-big{k}") for k in range(2)]

    before = len(log_lines())
    sent = []
    window_start = None
    window_end = None
    for group, text, creator in plan:
        if group == "limited":
            if window_start is None:
                window_start = time.perf_counter()
        r = submit(text, creator)
        if group == "limited":
            window_end = time.perf_counter()
        sent.append({"group": group, "creator": creator, "status": r["status"],
                     "request_id": r["request_id"], "timeout": r["timeout"]})

    new_lines = log_lines()[before:]
    entries = [json.loads(line) for line in new_lines]

    observed = Counter(s["status"] for s in sent)
    logged = Counter(e["status"] for e in entries)
    expected = Counter({200: 12, 422: 3, 413: 2, 429: 3})
    response_ids = {s["request_id"] for s in sent if s["request_id"]}
    log_ids = {e["request_id"] for e in entries}
    fields_ok = all(all(f in e for f in REQUIRED_FIELDS) for e in entries)
    cpu_ok = all(isinstance(e.get("cpu_ms"), (int, float)) and not isinstance(e.get("cpu_ms"), bool)
                 for e in entries if e.get("route") == "/submit")
    window_s = (window_end - window_start) if window_start and window_end else None

    checks = {
        "new_log_lines_is_20": len(entries) == 20,
        "response_status_distribution": observed == expected,
        "log_status_distribution": logged == expected,
        "request_ids_match_header": response_ids == log_ids and len(response_ids) == 20,
        "required_fields_present": fields_ok,
        "cpu_ms_numeric_for_submit": cpu_ok,
        "limited_requests_within_10s": window_s is not None and window_s <= 10,
    }
    met = all(checks.values())
    return {
        "trial": trial,
        "valid": True,
        "observed_status": {str(k): v for k, v in observed.items()},
        "logged_status": {str(k): v for k, v in logged.items()},
        "limited_window_s": round(window_s, 2) if window_s else None,
        "checks": checks,
        "result": "meets target" if met else "misses target",
    }


def run_crit1(trials):
    srv = Server("crit1")
    srv.start()
    try:
        return [crit1_trial(t) for t in range(1, trials + 1)]
    finally:
        srv.stop()


# ── criteria 2 and 3: cold start, then warm requests in the same session ─────

def crit23_trial(trial):
    srv = Server(f"crit23-t{trial}")
    srv.start()
    try:
        health = requests.get(f"{BASE}/health", timeout=5).json()
        if health.get("detector_loaded") is not False:
            return {"trial": trial, "valid": False,
                    "reason": f"/health reported detector_loaded={health.get('detector_loaded')} before first /submit"}

        before = len(log_lines())
        cold = submit(OWN[0], f"cold-t{trial}")
        cold_ok = cold["status"] == 200 and cold["elapsed_s"] <= 8
        cold_result = {"status": cold["status"], "elapsed_s": round(cold["elapsed_s"], 3),
                       "result": "meets target" if cold_ok else "misses target"}

        warm_ids = []
        for i in range(30):
            text = WARM_TEXTS[i % len(WARM_TEXTS)]
            r = submit(text, f"warm-t{trial}-{i}")
            warm_ids.append(r["request_id"])

        entries = {}
        for line in log_lines()[before:]:
            e = json.loads(line)
            entries[e["request_id"]] = e
        durations = [entries[rid]["duration_ms"] for rid in warm_ids if rid in entries]
        if len(durations) != 30:
            warm_result = {"valid_samples": len(durations), "result": "invalid (missing log lines)"}
        else:
            p = p95(durations)
            warm_result = {"p95_ms": round(p, 2), "samples": 30,
                           "result": "meets target" if p <= 250 else "misses target"}
        return {"trial": trial, "valid": True, "cold": cold_result, "warm": warm_result}
    finally:
        srv.stop()


def run_crit23(trials):
    return [crit23_trial(t) for t in range(1, trials + 1)]


# ── criterion 4: sustained load at 10 requests per second ────────────────────

def load_request(k, trial, attempt):
    text = LOAD_TEXTS[k % len(LOAD_TEXTS)]
    creator = f"load-t{trial}-a{attempt}-{k}"
    t_send = time.perf_counter()
    try:
        r = requests.post(f"{BASE}/submit", json={"text": text, "creator_id": creator}, timeout=30)
        elapsed = time.perf_counter() - t_send
    except requests.Timeout:
        return {"k": k, "t_send": t_send, "elapsed_s": time.perf_counter() - t_send,
                "status": None, "timeout": True, "body_ok": False}
    except requests.RequestException as exc:
        return {"k": k, "t_send": t_send, "elapsed_s": time.perf_counter() - t_send,
                "status": None, "timeout": False, "body_ok": False, "error": str(exc)}
    body_ok = False
    try:
        body = r.json()
        score = body.get("combined_score")
        body_ok = (r.status_code == 200
                   and body.get("guess") in ("human", "unsure", "ai")
                   and isinstance(score, (int, float)) and not isinstance(score, bool)
                   and 0 <= score <= 1)
    except ValueError:
        pass
    return {"k": k, "t_send": t_send, "elapsed_s": elapsed, "status": r.status_code,
            "timeout": False, "body_ok": body_ok}


def load_attempt(trial, attempt):
    srv = Server(f"crit4-t{trial}-a{attempt}")
    srv.start()
    try:
        results = []
        with cf.ThreadPoolExecutor(max_workers=200) as ex:
            t0 = time.perf_counter()
            cpu0 = time.process_time()
            futures = []
            for k in range(600):
                target = t0 + k * 0.1
                delay = target - time.perf_counter()
                if delay > 0:
                    time.sleep(delay)
                futures.append(ex.submit(load_request, k, trial, attempt))
            results = [f.result() for f in futures]
            cpu1 = time.process_time()
    finally:
        srv.stop()

    sends = sorted(r["t_send"] for r in results)
    rate = 600 / (sends[-1] - sends[0]) if sends[-1] > sends[0] else 0.0
    if rate < 9.5:
        return {"trial": trial, "attempt": attempt, "valid": False,
                "dispatch_rate_rps": round(rate, 3), "result": "invalid (rerun)"}

    completed = [r for r in results if r["status"] is not None]
    timeouts = sum(1 for r in results if r["timeout"])
    non200 = sum(1 for r in results if r["status"] != 200)
    five_xx = sum(1 for r in results if r["status"] is not None and 500 <= r["status"] <= 599)
    bodies_bad = sum(1 for r in results if not r["body_ok"])
    latency_p95 = p95([r["elapsed_s"] * 1000 for r in completed]) if len(completed) == 600 else None
    cpu_share = (cpu1 - cpu0) / (60 * os.cpu_count()) * 100

    met = (len(completed) == 600 and timeouts == 0 and non200 == 0 and bodies_bad == 0
           and latency_p95 is not None and latency_p95 <= 2000)
    return {
        "trial": trial,
        "attempt": attempt,
        "valid": True,
        "dispatch_rate_rps": round(rate, 3),
        "completed": len(completed),
        "timeouts": timeouts,
        "non_200": non200,
        "http_5xx": five_xx,
        "bodies_invalid": bodies_bad,
        "p95_latency_ms": round(latency_p95, 1) if latency_p95 is not None else None,
        "load_generator_cpu_share_pct": round(cpu_share, 3),
        "result": "meets target" if met else "misses target",
    }


def run_crit4(trials):
    out = []
    attempts_allowed = 5
    valid = 0
    attempt = 0
    while valid < trials:
        attempt += 1
        if attempt > attempts_allowed:
            raise RuntimeError(f"criterion 4: could not get {trials} valid trials in {attempts_allowed} attempts")
        result = load_attempt(valid + 1, attempt)
        out.append(result)
        if result["valid"]:
            valid += 1
    return out


# ── criterion 5: scoring regression ──────────────────────────────────────────

def environment_now():
    import torch
    import transformers
    from huggingface_hub.constants import HF_HUB_CACHE

    ref = Path(HF_HUB_CACHE) / "models--gpt2" / "refs" / "main"
    return {
        "python": platform.python_version(),
        "gpt2_revision": ref.read_text(encoding="utf-8").strip() if ref.exists() else None,
        "torch": torch.__version__.split("+")[0],
        "transformers": transformers.__version__,
    }


def environment_recorded():
    rec = {}
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        if line.startswith("python:"):
            rec["python"] = line.split(":", 1)[1].strip()
        elif line.startswith("gpt2_revision:"):
            rec["gpt2_revision"] = line.split(":", 1)[1].strip()
        elif line.startswith("torch=="):
            rec["torch"] = line.split("==", 1)[1].strip()
        elif line.startswith("transformers=="):
            rec["transformers"] = line.split("==", 1)[1].strip()
    return rec


def reference_entries():
    entries = json.loads(REF_FILE.read_text(encoding="utf-8"))["scores"]
    out = []
    for e in entries:
        text = scenario_texts(e["scenario"])[e["index"] - 1]
        sha8 = hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]
        if sha8 != e["text_sha8"]:
            raise RuntimeError(f"text lookup failed for {e['scenario']} #{e['index']}")
        out.append((e, text))
    return out


def crit5_trial(trial):
    now = environment_now()
    rec = environment_recorded()
    mismatch = {k: {"recorded": rec.get(k), "now": now.get(k)}
                for k in ENV_KEYS if rec.get(k) != now.get(k)}
    if mismatch:
        return {"trial": trial, "valid": False, "environment_mismatch": mismatch,
                "result": "invalid (environment does not match; restore and rerun)"}

    pairs = reference_entries()
    srv = Server(f"crit5-t{trial}")
    srv.start()
    try:
        rows = []
        for n, (e, text) in enumerate(pairs):
            r = submit(text, f"reg-t{trial}-{n}")
            body = r["body"] or {}
            score = body.get("combined_score")
            score_ok = (r["status"] == 200 and isinstance(score, (int, float))
                        and abs(score - e["combined_score"]) <= 0.001)
            label_ok = body.get("guess") == e["guess"]
            rows.append({"scenario": e["scenario"], "index": e["index"],
                         "reference_score": e["combined_score"], "score": score,
                         "reference_guess": e["guess"], "guess": body.get("guess"),
                         "pass": bool(score_ok and label_ok)})
    finally:
        srv.stop()
    met = len(rows) == 27 and all(row["pass"] for row in rows)
    return {"trial": trial, "valid": True, "texts": len(rows),
            "failing": [row for row in rows if not row["pass"]],
            "result": "meets target" if met else "misses target"}


def run_crit5(trials):
    return [crit5_trial(t) for t in range(1, trials + 1)]


# ── setup check (sends no requests) ──────────────────────────────────────────

def check_setup():
    problems = []
    now = environment_now()
    rec = environment_recorded()
    print("environment now:     ", now)
    print("environment recorded:", rec)
    for k in ENV_KEYS:
        if rec.get(k) != now.get(k):
            problems.append(f"environment {k}: recorded {rec.get(k)!r}, now {now.get(k)!r}")
    try:
        pairs = reference_entries()
        print(f"reference entries: {len(pairs)} (all sha8 checks passed)")
    except RuntimeError as exc:
        problems.append(str(exc))
    lengths = [len(t) for t in WARM_TEXTS]
    print("warm text lengths:", lengths)
    if not all(300 <= n <= 500 for n in lengths):
        problems.append("a warm-request text is outside 300-500 characters")
    if "AI201_RATE_LIMITS" in os.environ:
        problems.append("AI201_RATE_LIMITS is set; criteria assume the default (limiter on)")
    print("problems:", problems or "none")
    return not problems


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Run the Unit 9 criteria.")
    ap.add_argument("--check", action="store_true", help="verify setup only; send no requests")
    ap.add_argument("--criterion", choices=["1", "2", "3", "4", "5", "all"], default="all")
    ap.add_argument("--trials", type=int, default=3)
    args = ap.parse_args()

    if args.check:
        sys.exit(0 if check_setup() else 1)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = {"started": stamp, "python": platform.python_version(), "cpu_count": os.cpu_count()}
    want = {"1", "2", "3", "4", "5"} if args.criterion == "all" else {args.criterion}

    if "1" in want:
        results["criterion_1"] = run_crit1(args.trials)
    if want & {"2", "3"}:
        results["criteria_2_3"] = run_crit23(args.trials)
    if "4" in want:
        results["criterion_4"] = run_crit4(args.trials)
    if "5" in want:
        results["criterion_5"] = run_crit5(args.trials)

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    out = RUNS_DIR / f"unit9_run_{stamp}.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")

    for key, rows in results.items():
        if not isinstance(rows, list):
            continue
        print(f"\n{key}")
        for row in rows:
            print("  ", json.dumps(row))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
