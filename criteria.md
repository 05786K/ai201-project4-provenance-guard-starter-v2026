# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---

## Terms used below

- **Calibration set:** a fixed collection of test texts, written down once and reused unchanged, that is used to evaluate whether the detector produces all three `guess` values (`human`, `unsure`, `ai`). It contains human-written texts, clearly AI-generated texts, and borderline texts, and it is stored in `scenarios.py`.
- **Evaluation trial:** one complete run of every text in the calibration set through `POST /submit`. Each criterion must hold in all three trials.
- **AI-likeness score:** the `combined_score` field logged for each submission (0.0 = confidently human, 1.0 = confidently AI).

## 1. False Positives

Of 10 human-written calibration texts, no more than 2 may receive `guess: "ai"` (the "This text shows patterns commonly associated with AI-generated writing…" label) in each of the three evaluation trials.

**Why this target:**

A false accusation can harm a real writer's reputation. I allow at most 2 errors in 10 because avoiding false accusations matters more than catching every AI-generated text.

---

## 2. Score Spread

Across 5 clearly AI-generated texts and 5 clearly human-written texts, the average AI-likeness score for the AI texts must be at least 0.20 higher in each of the three evaluation trials.

**Why this target:**

My combined score is `0.70 * model + 0.30 * style`, and the unsure band is 0.30 wide (0.35 to 0.65). A 0.20 gap between group averages means a typical AI text and a typical human text land in clearly different parts of that range, rather than both sitting inside the unsure band. My calibration runs showed the model signal scoring clear-AI and clear-human text almost identically (0.8479 vs 0.8418), so this target is deliberately demanding: it checks that the combined score separates the groups at all, without requiring perfect detection.

---

## 3. Label Coverage

Each of the three `guess` values returned by `/submit`—`human` (score ≤ 0.35), `unsure` (between 0.35 and 0.65), and `ai` (score ≥ 0.65)—must appear at least once across the calibration set in each evaluation trial.

**Why this target:**

The `human` label needs a combined score of 0.35 or lower, but my style signal tends to sit around 0.4 to 0.5 and contributes 30% of the score, so `human` is only reachable when the model signal is low (roughly 0.30 or below when the style signal is about 0.45; in my sample log a model score of 0.1395 reached `human` but 0.3633 did not). If a label never appears, it is unreachable in practice, and a writer who should be told "probably written by a person" would only ever see "unsure". That is the failure this target is meant to catch.

---

## 4. Appeal Path

When an appeal is submitted for an existing content_id with a non-empty reasoning field, the API must return HTTP 200, record the appeal in the audit log with status under_review, and preserve the original decision. An appeal for a nonexistent content_id must return HTTP 404.

**Why this target:**

Writers need a traceable way to challenge incorrect results. Recording the appeal as a separate audit entry preserves the original decision and makes the review process verifiable.

---

## 5. Bad Input
Requests with missing `text`, empty or whitespace-only `text` must return HTTP `422`. Requests with text exceeding the maximum length of 10,000 characters must return HTTP `413`. The service must remain running after each rejected request.

**Why this target:**

Every `/submit` request runs GPT-2 locally, so an enormous text costs real compute and memory; the 10,000-character cap (413) protects the service from that. Missing or empty `text` is a different mistake by the caller (422), and an empty string would otherwise be scored and logged as if it were a real submission, putting a meaningless decision in the audit log. Distinct codes let a tester tell the two cases apart.


---

# Unit 9 — Capstone Criteria

**Everything above this line is Unit 7 and Unit 8 and is left unchanged. From this point forward, this file is about Unit 9.** The five criteria that follow are numbered 1 to 5 on their own, independent of the five above.

## 1. Operational Log Completeness

In each of 3 independent trials, send a controlled batch of exactly 20 `/submit` HTTP requests. Each batch must produce exactly 20 new records in `logs/requests.jsonl`, with the following status distribution:

- 12 requests returning HTTP 200
- 3 requests returning HTTP 422
- 2 requests returning HTTP 413
- 3 requests returning HTTP 429

The 12 HTTP 200 requests use texts from `scenarios.py`'s "my own writing" scenario (indices 1–9, repeating as needed). The 3 HTTP 422 requests use an empty `text`. The 2 HTTP 413 requests use `text` of 10,001 `x` characters.

Generate the three HTTP 429 responses by sending 9 requests within 10 seconds using the same limited `creator_id` for that trial, exceeding the 6-per-minute limit. Use a different limited creator ID for each trial:

- Trial 1: `log-test-limited-1`
- Trial 2: `log-test-limited-2`
- Trial 3: `log-test-limited-3`

Of the 9 limited-creator requests, the first 6 return HTTP 200 and count toward the 12 HTTP 200 requests; the other 3 return HTTP 429. The remaining 11 requests use other creator IDs: 6 return HTTP 200, 3 return HTTP 422, and 2 return HTTP 413. Across the batch, that gives 12 HTTP 200, 3 HTTP 422, 2 HTTP 413 and 3 HTTP 429, for 20 requests in total.

For each trial, count only the 20 log lines appended during that trial's batch. Do not include records from previous trials. Do not send any other requests to the application during the batch, including `/health` requests.

Every log record must contain the following fields:

- `ts`
- `request_id`
- `route`
- `status`
- `outcome`
- `duration_ms`
- `cpu_ms`

The `request_id` in each record must match the corresponding response's `X-Request-ID` header. The `cpu_ms` field must be present and contain a numeric value for every `/submit` record, including rejected requests.

**Reason:** Unit 8 exposed that rejected requests were not consistently recorded. Missing records compromise request counts and failure analysis. Requiring CPU time for every request also verifies that rejected requests are included in operational measurements.

## 2. Cold-Start Performance

In each of 3 independent trials, restart the application using the documented Waitress startup command. Before the first `/submit` request, verify that `/health` reports `detector_loaded: false`.

The first `/submit` request after each restart must return HTTP 200 within 8 seconds, measured using client-side wall-clock time.

Each trial restarts the application on the same machine without rebooting it. The model files may therefore remain in the operating system's file cache. This criterion measures an application restart, not a machine reboot.

**Reason:** GPT-2 loads lazily. Previous observations ranged from 5.3 to 9.0 seconds. The 8-second target challenges cold-start performance while confirming that the detector is initially unloaded.

## 3. Warm-Request Performance

In each of 3 independent trials, use the same trial as Criterion 2. Immediately after the cold-start `/submit` request returns HTTP 200, send 30 sequential `/submit` requests using the "my own writing" texts at indices 1, 3, 4, 5, 6, 7, 8, 9 and 10 from `scenarios.py` (index 2 is 527 characters and is excluded), cycled in that order to reach 30 requests.

Use a distinct `creator_id` for each request to avoid triggering the per-creator rate limit. Exclude the initial cold-start request from the measurement.

The 95th-percentile (`p95`) server-side `duration_ms` must be no greater than 250 ms in each trial. Compute p95 using the nearest-rank method: sort the 30 `duration_ms` values in ascending order and use the 29th value.

**Reason:** Previous warm-request measurements showed a p95 of approximately 115 ms. A 250 ms target allows reasonable variation while still detecting meaningful performance regressions.

## 4. Load and Failure Behavior

In each of 3 independent valid trials, send exactly 600 `/submit` requests at a target rate of 10 requests per second.

Each request uses one of the "my own writing" texts (indices 1–10), cycling in order. Dispatch requests concurrently at a steady rate of one every 100 ms. Do not wait for an earlier request to complete before dispatching the next request. Allow multiple requests to remain in flight simultaneously.

Record the actual client-side send time for every request. Calculate the dispatch rate by dividing the total number of requests sent by the elapsed time between the first and last recorded send times. If the client dispatches fewer than 9.5 requests per second, mark the trial invalid and rerun it. An invalid trial is replaced by its rerun and does not count toward the three required valid trials.

All 600 requests must return HTTP 200 with valid JSON response bodies containing:

- `guess`: one of `human`, `unsure`, or `ai`.
- `combined_score`: a numeric value between 0 and 1, inclusive.

Set the client-side request timeout to 30 seconds. Require:

- Exactly 600 completed HTTP responses.
- Zero client-side timeouts.
- Zero non-200 HTTP responses, including HTTP 5xx responses.
- Client-side p95 latency no greater than 2,000 ms.

Compute p95 using the nearest-rank method. With 600 completed requests, use the 570th value after sorting the client-side response times in ascending order.

Use a unique `creator_id` for every request to avoid triggering the per-creator rate limit.

Run the load generator on the same machine as the application server. Measure the load generator's CPU time using Python's `time.process_time()`, which measures user and system CPU time consumed by the current process. Calculate its CPU share as:

`(load generator process CPU time in seconds / (60 seconds × number of logical CPU cores)) × 100`

Record this percentage for each trial alongside the latency results. CPU share is reported for context and does not determine whether the criterion passes or fails.

**Reason:** Earlier development measurements showed approximately 0.7–1.4 CPU-seconds per request. At 10 requests per second, that implies roughly 7–14 CPU-seconds of work per second. This test examines queueing, latency, and failures under that demand. The 1 request-per-second baseline represents approximately 1.4 CPU-seconds of work per second at the upper observed estimate, a relatively light load on the 16-thread development machine. Recording the load generator's CPU share helps interpret the latency results because it shares the machine's processing resources.



## 5. Unit 8 Scoring Regression

In each of 3 independent trials, run all 27 reference texts in `results/unit8_reference_scores.json` through `/submit`.

Each reference entry's `scenario` and `index` fields locate its text in `scenarios.py`; recomputing its SHA-256 and checking the first 8 hex characters match `text_sha8` confirms the right text was found before submitting it.

For every reference text:

- The resulting `combined_score` must be within ±0.001 of its original Unit 8 reference score.
- The resulting `guess` label must exactly match its original Unit 8 reference label.

Use the same Python version, GPT-2 model revision, PyTorch (`torch`) version, and Transformers version recorded in `results/unit8_environment.txt`.

Create `results/unit8_environment.txt` by running `pip freeze` from the original project `.venv` that produced the Unit 8 reference scores. Add the following two metadata lines manually at the top of the file:

- `python: 3.13.13`
- `gpt2_revision: 607a30d783dfa663caf39e06633721c8d4cfcd7e`

The regression check must compare the Python version, GPT-2 revision, `torch` version, and `transformers` version. Other package entries in the environment snapshot are retained as supporting environment evidence but are not required to match for this criterion.

A version that does not match invalidates the trial rather than failing the criterion; rerun after restoring the matching environment.

**Reason:** Unit 9 instrumentation should not change the detector's scoring behavior. Verifying the Python, model revision, and scoring-library versions helps ensure that differences in scores are caused by code changes rather than changes to the scoring environment.