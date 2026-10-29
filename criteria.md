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

## 1. False Positives

Of 10 human-written calibration texts, no more than 2 may receive the `Potentially AI-generated` label in each of the three evaluation trials.

**Why this target:**

A false accusation can harm a real writer's reputation. I allow at most 2 errors in 10 because avoiding false accusations matters more than catching every AI-generated text.

---

## 2. Score Spread

Across 5 clearly AI-generated texts and 5 clearly human-written texts, the average AI-likeness score for the AI texts must be at least 0.20 higher in each of the three evaluation trials.

**Why this target:**

The scores should show a meaningful difference between the two groups without requiring perfect detection. A 0.20 gap is a challenging but reasonable initial target.

---

## 3. Label Coverage

Each of the three labels—`Likely human-written`, `Insufficient evidence`, and `Potentially AI-generated`—must appear at least once across the calibration set in each evaluation trial.

**Why this target:**

Every label should be reachable. If a label never appears, the scoring thresholds may be poorly chosen or that outcome may be impossible to produce.

---

## 4. Appeal Path

When an appeal is submitted for an existing content_id with a non-empty reasoning field, the API must return HTTP 201, record the appeal in the audit log with status under_review, and preserve the original decision. An appeal for a nonexistent content_id must return HTTP 404.

**Why this target:**

Writers need a traceable way to challenge incorrect results. Recording the appeal as a separate audit entry preserves the original decision and makes the review process verifiable.

---

## 5. Bad Input
Requests with missing `text`, empty or whitespace-only `text` must return HTTP `422`. Requests with text exceeding the maximum length of 10,000 characters must return HTTP `413`. The service must remain running after each rejected request.

**Why this target:**

Invalid input should be rejected predictably without breaking the API. Specific status codes make errors easier to test and help developers understand why a request failed.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
