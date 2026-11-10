# Running Provenance Guard

This is the run path for Unit 9. It runs on your own machine (Path B, local with
logs). Nothing is hosted and no account or API key is needed.

The starter's general guide to the code, the routes and the units is still in
git history, in the version of this file before the Unit 9 rewrite. This file
covers only how to start the service and check that it works.

---

## What you need

| Item | Value |
|---|---|
| Python | 3.11, 3.12 or 3.13. **Not 3.14.** Tested on 3.13.13 |
| Operating system | Windows (tested), macOS and Linux should work the same |
| Dependencies | pinned in `requirements.txt`: Flask, Flask-Limiter, requests, transformers, torch, waitress, certifi (plus gunicorn, unused here) |
| Model | `gpt2`, downloaded from Hugging Face on first use. Its weights file `model.safetensors` is **548,105,171 bytes (about 548 MB)** |
| Disk | about 550 MB for the model, plus the Python packages (torch is the largest) |
| Network | needed once, to download the model and packages |

The model runs on the CPU. No GPU is needed.

---

## Setup (once)

Run these from the project folder.

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python detector.py
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python detector.py
```

`python detector.py` downloads the model the first time (about 550 MB) and scores
a sample sentence. You only need to do it once per machine.

---

## Start the service

```bash
python serve.py
```

It prints the address and then waits. Leave this terminal open. Stop the service
with `Ctrl+C`.

`serve.py` runs the service with **waitress**, a production-style server that
works on Windows. It runs one process with no auto-reloader, so the model is loaded
once.

By default the service listens only on your own machine, at
`http://127.0.0.1:5000`.

---

## Check that it works

In a second terminal, run:

**Windows (PowerShell), one line:**

```powershell
curl.exe -X POST http://127.0.0.1:5000/ping -H "Content-Type: application/json" -d '{\"message\": \"hello\"}'
```

You should get back `{"ok":true,"service":"provenance-guard","you_sent":"hello"}`.

**macOS / Linux / Git Bash:**

```bash
curl -X POST http://127.0.0.1:5000/ping \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```

Then check the scoring route:

```powershell
curl.exe -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{\"text\": \"Technology plays an important role in modern education. Online learning platforms provide students with access to educational resources.\", \"creator_id\": \"me\"}'
```

**The first `/submit` after startup is slow: about 5 to 6 seconds.** That is the
model loading into memory. Later requests take about 0.1 seconds. Plan for it
when you test.

---

## Where the records go

Every request writes one line to `logs/requests.jsonl`. This is the ops log: one
JSON object per request, including rejected and failed ones. Each line has
`ts`, `request_id`, `route`, `status`, `outcome`, `duration_ms`, per-stage times
in `stage_ms`, `cpu_ms`, `model_cold`, and the scores for `/submit`. The raw text
is never written, only its length and a short hash.

Every request also gets an `X-Request-Id` response header, so a response can be
matched to its log line.

Decisions go to `logs/audit.jsonl`, the audit log from Units 7 and 8. Appeals go
there too, and the two logs link through `content_id`.

To summarise the ops log:

```bash
python summarize_log.py
```

It prints counts by route and status, error and rejection counts, cold and warm
latency, the share of time in each stage, and CPU per request.

---

## Settings

Set these as environment variables before `python serve.py`. Leave them unset for
the defaults.

| Variable | Default | What it does |
|---|---|---|
| `HOST` | `127.0.0.1` | Loopback, your machine only. Use `0.0.0.0` only if you want other machines to reach it |
| `PORT` | `5000` | The port |
| `AI201_THREADS` | `4` | Request threads inside the one process |
| `AI201_RATE_LIMITS` | `1` | `1` turns the per-creator rate limit on (6 per minute, 120 per day). `0` turns it off |
| `AI201_OPS_LOG` | `logs/requests.jsonl` | Where the ops log is written |

---

## Routes

| Route | What it does |
|---|---|
| `POST /ping` | Liveness check |
| `GET /health` | Service up, and whether the model is loaded yet |
| `POST /submit` | Score a piece of text. Body: `{"text": "...", "creator_id": "..."}` |
| `POST /appeal` | Appeal a decision. Body: `{"content_id": "...", "reasoning": "..."}` |
| `GET /log` | The audit log as JSON |

---

## When something goes wrong

| What you see | What to do |
|---|---|
| `ModuleNotFoundError` | The virtual environment isn't active, or `pip install -r requirements.txt` didn't finish |
| `DetectorUnavailable` on `/submit` | Run `python detector.py` once to download the model. It needs network access |
| `Address already in use` | Another copy of the service is still running. Stop it, or set `PORT` to another number |
| `422` on `/submit` | Your body was missing `text`, or `text` was empty. The response says which |
| `413` on `/submit` | `text` is longer than 10,000 characters |
| `429` on `/submit` | You've sent more than 6 requests a minute under one `creator_id`. Wait a minute, or set `AI201_RATE_LIMITS=0` |
| `curl` gives an error about `Headers` | You're in PowerShell, where `curl` isn't curl. Use `curl.exe`, on one line |
| Every request is slow | Check `GET /health`. If `detector_loaded` is `false`, the model isn't loaded yet |

---

## Notes for running on a fresh machine

The model is cached under your user folder (for example `~/.cache/huggingface`).
A clean clone of this repository reuses that cache, so it doesn't re-download the
model. On a machine with no cache, the first `python detector.py` downloads about
550 MB.

`python test.py` writes a `/ping` line to the ops log, because it checks the
service. If you're about to make a recorded run, delete `logs/requests.jsonl`
first.

---

## Why this is local and not hosted

A free hosted tier gives 512 MB of memory. The model file alone is about 548 MB,
before Python, torch and Flask are loaded. So the service can't fit a free tier,
and a free host also wipes its disk when it sleeps, so the model would download
again each time. This is why the unit uses the local path.
