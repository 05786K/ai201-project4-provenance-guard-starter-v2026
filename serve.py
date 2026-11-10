#!/usr/bin/env python3
"""
Run Provenance Guard as a real server — UNIT 9.

    python serve.py

This is the documented start command (see RUNNING.md). It serves the same `app`
as `python app.py`, using waitress, a production-style server that runs on
Windows, macOS and Linux.

Why not `python app.py`? That runs Flask's development server, and in debug
mode it starts a reloader, which loads GPT-2 twice. Here there is no reloader:
one process, one copy of the model.

Settings come from the environment, with defaults:

    HOST              127.0.0.1   loopback only; set 0.0.0.0 to accept other machines
    PORT              5000
    AI201_THREADS     4           request threads in this process

The model loads lazily on the first /submit, so that first request is slow
(about 5 to 6 seconds). Later requests are not. See RUNNING.md.
"""

import os
import sys

from waitress import serve

import config
from app import app

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass


def main() -> None:
    threads = int(os.getenv("AI201_THREADS", "4"))
    print(f"Provenance Guard (waitress) on http://{config.HOST}:{config.PORT}")
    print(f"  threads:         {threads}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  ops log:         {config.OPS_LOG}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print()
    print("Check it's alive (Windows PowerShell):")
    print(f'  curl.exe -X POST http://{config.HOST}:{config.PORT}/ping -H "Content-Type: application/json" -d "{{\\"message\\": \\"hello\\"}}"')
    print()
    serve(app, host=config.HOST, port=config.PORT, threads=threads)


if __name__ == "__main__":
    main()
