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

# Unit 9 — Capstone

**Everything above this line is Unit 7 and Unit 8 and is left unchanged. From this point forward, this file is about Unit 9.** The five Unit 9 criteria that follow are numbered 1 to 5 on their own, independent of the five above.
