# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.
>
> **Unit 9 (capstone) sections:** [What This Extends](#unit-9--what-this-extends) · [The Shape](#unit-9--the-shape) · [Running It](#unit-9--running-it) · [Instrumentation](#unit-9--instrumentation) · [What It Costs](#unit-9--what-it-costs). They are at the bottom of this file, after Unit 8's "What's Still Broken".

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does
Provenance Guard is a writing assessment tool that analyzes submitted text and assigns one of three labels: `human`, `unsure`, or `ai`. The submission follows this path:

1. **API (`app.py`)** — Receives a writing submission through the `/submit` endpoint and processes the request.
2. **Detector (`detector.py`)** — Uses a local GPT-2 language model to measure text predictability and converts perplexity into an AI-likeness score.
3. **Stylometry (`stylometry.py`)** — Measures writing characteristics, including sentence-length variation, vocabulary diversity, and punctuation density.
4. **Scoring (`scoring.py`)** — Combines the model signal (70%) and style signal (30%) into one overall score.
5. **Confidence field** — Returns a confidence value with the assessment. The current value is a placeholder (`0.5`), not a calibrated estimate of reliability.
6. **Labeling (`scoring.py`)** — Applies the configured thresholds to assign one of three labels: `human`, `unsure`, or `ai`.
7. **Response and appeal (`app.py`, `audit.py`)** — Returns the assessment and its explanation, records the decision in an append-only audit log, and provides an appeal endpoint so writers can challenge an assessment.

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:**

The model signal uses GPT-2 to calculate the perplexity of the submitted text. Perplexity measures how predictable a sequence of words is to a language model. The implementation converts perplexity into a score from 0 to 1. A higher score means the text is more predictable to GPT-2 and is treated by this heuristic as more AI-like.

**Why that might differ between human and AI writing:**

AI-generated text often follows common language patterns and uses statistically likely word sequences, which can make it more predictable to a language model. Human writing may contain more unusual word choices, personal phrasing, or unexpected transitions, which can make it less predictable. However, this is only a tendency: human writing can also be highly predictable, and AI writing can be made less predictable through editing.

**What it can't see:**

The model signal cannot identify the author or establish whether a person or an AI system actually wrote the text. It cannot see the writer's identity, intent, drafting process, or use of AI tools. It only measures how predictable the text is to GPT-2. Short, conventional, or formal human writing may receive a high AI-like score, while edited or unusual AI-generated text may receive a lower score. The score is therefore a heuristic, not a probability or proof of authorship.

### Signal two — the style signal

**What it measures:**

The style signal measures statistical features of the text's structure and vocabulary rather than its meaning. The current implementation uses two measures:

- **Sentence-length spread:** Calculates the standard deviation of sentence word counts divided by their mean. It measures how much sentence lengths vary relative to the average.
- **Type-token ratio:** Calculates the number of unique words divided by the total number of words. It measures vocabulary diversity.

The implementation converts these measures into two component scores and averages them. Lower sentence-length variation and lower vocabulary diversity increase the AI-likelihood score. Punctuation density is also calculated (selected punctuation marks divided by total characters), but it is not currently included in `style_signal()`.

**Why that might differ between human and AI writing:**

AI-generated prose may use more consistent sentence lengths and repeat a narrower range of vocabulary. Human writing may be less uniform, with a wider mix of short and long sentences and more varied word choices. Sentence-length spread and type-token ratio can therefore provide clues about writing style. These are tendencies, not dependable distinctions: humans can write uniformly, and AI can produce varied sentence lengths and vocabulary.

**What it can't see:**

The style signal cannot understand the text's meaning, context, factual accuracy, or the author's identity. It cannot determine whether AI was used. It only measures surface-level patterns. Those patterns can be changed without changing the underlying ideas—for example, by adding typos, splitting or combining sentences, repeating or replacing words, or inserting quotations. Such changes can manipulate the score, which is a key blind spot relevant to Unit 8's attack set. The measures can also be unstable on short texts; for example, a one-sentence submission has a sentence-length spread of 0. The current score also excludes punctuation density, so punctuation changes alone do not affect `style_signal()`.

### The combining rule

**The rule:**

Provenance Guard uses a weighted average to combine the model signal and style signal. When the two signals disagree, the weighted average balances their scores, giving more influence to the model signal.

**The numbers:**
- Model signal: 70%
- Style signal: 30%

`combined_score = (0.70 * model_score) + (0.30 * style_score)`

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**

In testing, the clearly AI-written sample received a model score of 0.7581 and a style score of 0.4928. The clearly human-written sample received a model score of 0.8442 and a style score of 0.4916.

The model signal rated the human-written sample as more AI-like, while the style signal gave nearly identical scores to both samples. Our weighted average gives 70% weight to the model signal and 30% to the style signal, so the combined score follows the model signal more strongly while still incorporating the style signal.

---
### Calibration Results

During calibration, both signals were tested against clearly AI-written, clearly human-written, formal human, and lightly edited AI text.

| Test input | Model signal | Style signal |
|---|---:|---:|
| Clearly AI | 0.8479 | 0.5551 |
| Clearly human | 0.8418 | 0.4678 |
| Formal human | 0.8838 | 0.4375 |
| Lightly edited AI | 0.7907 | 0.4417 |

**What I discovered:**

Neither signal consistently distinguished human-written text from AI-generated text. The model signal assigned the formal human sample the highest AI-likelihood score. The clearly AI and clearly human samples also received very similar model scores.

The style signal produced overlapping scores across the test categories. This demonstrates that the signals are imperfect heuristics and that combining them does not automatically eliminate false positives.

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00–0.35 | We think this text was probably written by a person. However, this result cannot guarantee who wrote it. |
| unsure | Above 0.35 and below 0.65 | We cannot confidently determine whether this text was written by a person or AI. |
| high-confidence AI | 0.65–1.00 | This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used. |

**Why I worded the "unsure" one this way:**

I chose wording that communicates uncertainty without accusing the writer of using AI. The person reading the result may have written every word themselves. The system only identifies patterns in writing; it cannot prove who wrote the text.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

```bash
$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"text": "Artificial intelligence is changing many industries. Businesses use these systems to automate repetitive tasks and improve efficiency. Organizations must consider accuracy, privacy, and responsible use.", "creator_id": "test-user"}'
```

```json
{
  "combined_score": 0.5038079592741808,
  "confidence": 0.5,
  "content_id": "a1206013-0c2a-45a0-a7c4-ed1ec4bedafb",
  "guess": "unsure",
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "model_score": 0.538,
  "style_score": 0.424026530913936
}
```

**An appeal** (against the same `content_id`)

```bash
$ curl -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d '{"content_id": "a1206013-0c2a-45a0-a7c4-ed1ec4bedafb", "reasoning": "I wrote this text myself and believe the detector incorrectly classified it."}'
```

```json
{
  "content_id": "a1206013-0c2a-45a0-a7c4-ed1ec4bedafb",
  "message": "Your appeal has been submitted and is under review.",
  "status": "under_review"
}
```

**What the log shows afterwards** (`GET /log`, entries for this `content_id`)

```json
[
  {
    "combined_score": 0.5038079592741808,
    "content_id": "a1206013-0c2a-45a0-a7c4-ed1ec4bedafb",
    "creator_id": "test-user",
    "guess": "unsure",
    "label": "We cannot confidently determine whether this text was written by a person or AI.",
    "model_score": 0.538,
    "status": "decided",
    "style_score": 0.424026530913936,
    "timestamp": "2026-11-02T08:59:49+00:00"
  },
  {
    "content_id": "a1206013-0c2a-45a0-a7c4-ed1ec4bedafb",
    "creator_id": "test-user",
    "event": "appeal",
    "reasoning": "I wrote this text myself and believe the detector incorrectly classified it.",
    "status": "under_review",
    "timestamp": "2026-11-02T08:59:52+00:00"
  }
]
```




---

## How I Used AI

**Moment 1**
- *What I asked for:* Help understanding how to combine the GPT-2 model signal with the stylometric signal into one overall score.
- *What came back:* Guidance on using a weighted average to combine the two signals, with the model signal weighted at 70% and the style signal at 30%.
- *What I changed:* I implemented the combining logic in `scoring.py` using `combine_signals()` and stored the weights in `config.py`. I then tested the combined scoring behavior with different writing samples.

### Moment 2

**Moment 2**
- *What I asked for:* Help implementing the classification logic that converts the combined score into the required labels.
- *What came back:* Guidance on using score thresholds to determine which label should be assigned and on providing an explanation for each result.
- *What I changed:* I implemented `score_to_label()` in `scoring.py`, using the provided labels: `human`, `unsure`, and `ai`. I configured the thresholds in `config.py` and tested whether all three labels could be reached.

**Moment 3**
- *What I asked for:* Help reading the attack run and the eval run and diagnosing each failure by stage.
- *What came back:* A HELD or BROKE verdict for each of the 46 attacks I had to judge and a diagnosis grouped by the five stages.
- *What I changed:* I decided that a missing `creator_id` should fall back to the caller's address and that I would not add a minimum word count in input validation. 

---

## Rate Limiting

**My limits:** 6 per minute, 120 per day (`config.py::RATE_LIMIT_PER_MINUTE` and `RATE_LIMIT_PER_DAY`, applied to `/submit` in `app.py`).

**Why those numbers and not others:**
A real writer submits their own work a few times an hour. 6 per minute lets them fix a typo and resubmit several times in a row without hitting the wall, and 120 per day is about 5 an hour across a full day, far more than one person writing needs. A script mapping my thresholds needs hundreds of probes, so 120 per day caps it at a small fraction of that per creator, and 6 per minute means it takes at least 20 minutes just to spend them. The per-minute number also protects the service itself, because every request runs GPT-2 locally (one to two seconds each), so 6 per minute is a bounded amount of compute per caller. I did not go lower because a stricter limit would start rejecting a legitimate writer who resubmits a few revisions in a minute. The weakness: the limit is per `creator_id`, so a script that invents a new `creator_id` for every request gets a fresh allowance each time. I did not close that.

**What a caller counts as:** the `creator_id` in the request body, falling back to the caller's IP address when it is missing or not a string (`app.py::rate_limit_key`). Per `creator_id` means one script using one id is caught, but a script rotating ids is not. Per address would catch the rotating script but would lump a whole household or office into one caller. Requests with no usable `creator_id` all share their address's bucket; that is why RQ11 in the attack run returned 429 before its content was ever checked.

**The run of status codes when I pushed past it:**

`python run_attacks.py --flood 15`, saved to `results/flood_2026-11-04_1754.md`. The first 6 requests got 200 and the other 9 got 429, matching the 6 per minute limit. Each rejection is in the audit log with `reason: rate_limited`.

```
The first one is slow while the model loads.

  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 200
  [ 7/15] 429
  [ 8/15] 429
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
200 200 200 200 200 200 429 429 429 429 429 429 429 429 429
============================================================

9 of 15 were rate limited. Paste the run above into your README
under **Rate Limiting**, and check GET /log recorded the rejections.
```

---

## Attack Run — Before

`python run_attacks.py --label before --set attack_set`, written to `results/attack_run_2026-11-04_1753_before.md` (the same attacks and results as the earlier `results/attack_run_2026-11-04_1613.md`). All 56 attacks, each with its status, the service's guess and a HELD or BROKE mark.

Rules for the marks: BROKE means the attack achieved its goal (AI text called human, human text called AI, a confident label on garbage, a crash, or bad input accepted). HELD means the service resisted, stayed unsure, or rate-limited. The script auto-marked the 10 crashes BROKE and left 46 for me to judge; the marks on those 46 are my judgment.

| Family | Attacks | Auto-BROKE | My BROKE | HELD | Total BROKE | Which |
|---|---|---|---|---|---|---|
| evasion | 10 | 0 | 3 | 7 | 3 | EV01, EV05, EV08 (called human) |
| false_positive | 8 | 0 | 6 | 2 | 6 | FP02–FP07 (genuine human text called AI) |
| prompt_injection | 6 | 0 | 1 | 5 | 1 | PI02 (called human) |
| malformed | 20 | 10 | 7 | 3 | 17 | 10 crashes (500); MF03–MF07 confident labels on garbage; RQ02, RQ06 bad `creator_id` accepted |
| flood_same_creator | 12 | 0 | 0 | 12 | 0 | first 6 returned 200, last 6 returned 429 |
| **Total** | **56** | **10** | **17** | **29** | **27** | |

Full output:

```
 [ 1/56] EV01   evasion           200   human    BROKE
  [ 2/56] EV02   evasion           200   unsure   HELD
  [ 3/56] EV03   evasion           200   unsure   HELD
  [ 4/56] EV04   evasion           200   unsure   HELD
  [ 5/56] EV05   evasion           200   human    BROKE
  [ 6/56] EV06   evasion           200   unsure   HELD
  [ 7/56] EV07   evasion           200   unsure   HELD
  [ 8/56] EV08   evasion           200   human    BROKE
  [ 9/56] EV09   evasion           200   unsure   HELD
  [10/56] EV10   evasion           200   ai       HELD
  [11/56] FP01   false_positive    200   unsure   HELD
  [12/56] FP02   false_positive    200   ai       BROKE
  [13/56] FP03   false_positive    200   ai       BROKE
  [14/56] FP04   false_positive    200   ai       BROKE
  [15/56] FP05   false_positive    200   ai       BROKE
  [16/56] FP06   false_positive    200   ai       BROKE
  [17/56] FP07   false_positive    200   ai       BROKE
  [18/56] FP08   false_positive    200   human    HELD
  [19/56] PI01   prompt_injection  200   unsure   HELD
  [20/56] PI02   prompt_injection  200   human    BROKE
  [21/56] PI03   prompt_injection  200   unsure   HELD
  [22/56] PI04   prompt_injection  200   unsure   HELD
  [23/56] PI05   prompt_injection  200   unsure   HELD
  [24/56] PI06   prompt_injection  200   unsure   HELD
  [25/56] MF01   malformed         200   unsure   HELD
  [26/56] MF02   malformed         500   —        BROKE
  [27/56] MF03   malformed         200   human    BROKE
  [28/56] MF04   malformed         200   human    BROKE
  [29/56] MF05   malformed         200   ai       BROKE
  [30/56] MF06   malformed         200   ai       BROKE
  [31/56] MF07   malformed         200   ai       BROKE
  [32/56] MF08   malformed         200   ai       HELD
  [33/56] RQ01   malformed         500   —        BROKE
  [34/56] RQ02   malformed         200   human    BROKE
  [35/56] RQ03   malformed         500   —        BROKE
  [36/56] RQ04   malformed         500   —        BROKE
  [37/56] RQ05   malformed         500   —        BROKE
  [38/56] RQ06   malformed         200   human    BROKE
  [39/56] RQ07   malformed         500   —        BROKE
  [40/56] RQ08   malformed         500   —        BROKE
  [41/56] RQ09   malformed         500   —        BROKE
  [42/56] RQ10   malformed         500   —        BROKE
  [43/56] RQ11   malformed         429   —        HELD
  [44/56] RQ12   malformed         500   —        BROKE
  [45/56] FL01_01 flood_same_creator 200   human    HELD
  [46/56] FL01_02 flood_same_creator 200   human    HELD
  [47/56] FL01_03 flood_same_creator 200   human    HELD
  [48/56] FL01_04 flood_same_creator 200   human    HELD
  [49/56] FL01_05 flood_same_creator 200   human    HELD
  [50/56] FL01_06 flood_same_creator 200   human    HELD
  [51/56] FL01_07 flood_same_creator 429   —        HELD
  [52/56] FL01_08 flood_same_creator 429   —        HELD
  [53/56] FL01_09 flood_same_creator 429   —        HELD
  [54/56] FL01_10 flood_same_creator 429   —        HELD
  [55/56] FL01_11 flood_same_creator 429   —        HELD
  [56/56] FL01_12 flood_same_creator 429   —        HELD

============================================================
Wrote results\attack_run_2026-11-04_1753_before.md
  auto-marked BROKE: 10
  left for you:      46  (judged below: 29 HELD, 17 BROKE)
  final:             27 BROKE, 29 HELD
============================================================
```

**Twelve audit log entries from the run**

Taken from `logs/audit.jsonl` (the 16:13 run, 00:13 UTC). In order: three evasions
read as human (EV01, EV05, EV08), three false positives (FP03, FP06, FP07), the
injection that came back human (PI02), garbage scored confidently (MF04 punctuation,
MF06 emoji), two malformed requests logged as if valid (RQ02 empty `creator_id`,
RQ06 object `creator_id`), and one rate-limit rejection, which carries no
`content_id` or scores.

```json
{"timestamp": "2026-11-05T00:13:47+00:00", "content_id": "242a5bf5-4500-46aa-92f6-12e7754fcf49", "creator_id": "attacker_EV01", "guess": "human", "model_score": 0.1635, "style_score": 0.4954668754756913, "combined_score": 0.2630900626427074, "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.", "status": "decided"}
{"timestamp": "2026-11-05T00:13:47+00:00", "content_id": "31f6bdb8-c541-457e-9e56-c0f0510ee34c", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.4143144609464353, "combined_score": 0.3491343382839306, "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.", "status": "decided"}
{"timestamp": "2026-11-05T00:13:48+00:00", "content_id": "aa8c2ffd-52ac-49b4-86e2-899aee99dc89", "creator_id": "attacker_EV08", "guess": "human", "model_score": 0.2452, "style_score": 0.3897593953942288, "combined_score": 0.28856781861826863, "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.", "status": "decided"}
{"timestamp": "2026-11-05T00:13:49+00:00", "content_id": "cbdabe0c-9448-48a7-bfce-cf37443793e1", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.5150066988642605, "combined_score": 0.7180720096592782, "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.", "status": "decided"}
{"timestamp": "2026-11-05T00:13:49+00:00", "content_id": "dc996818-feb4-472d-950d-6a7b9e6d2acc", "creator_id": "attacker_FP06", "guess": "ai", "model_score": 0.8814, "style_score": 0.4619408908912053, "combined_score": 0.7555622672673615, "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.", "status": "decided"}
{"timestamp": "2026-11-05T00:13:49+00:00", "content_id": "521194a3-ba5d-4f44-b922-3aa0f2374234", "creator_id": "attacker_FP07", "guess": "ai", "model_score": 0.8816, "style_score": 0.5600513751364047, "combined_score": 0.7851354125409213, "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.", "status": "decided"}
{"timestamp": "2026-11-05T00:13:50+00:00", "content_id": "84bd0d2e-3f69-4f5a-b6e3-712f400b32f6", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.32491589015512873, "combined_score": 0.2405547670465386, "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.", "status": "decided"}
{"timestamp": "2026-11-05T00:13:51+00:00", "content_id": "89a82660-5b80-4646-b677-9b9a42cdc18d", "creator_id": "attacker_MF04", "guess": "human", "model_score": 0.0112, "style_score": 1.0, "combined_score": 0.30784, "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.", "status": "decided"}
{"timestamp": "2026-11-05T00:13:52+00:00", "content_id": "7e66f1e2-7ce7-48d1-aac2-bff28ca12384", "creator_id": "attacker_MF06", "guess": "ai", "model_score": 0.9969, "style_score": 1.0, "combined_score": 0.99783, "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.", "status": "decided"}
{"timestamp": "2026-11-05T00:13:52+00:00", "content_id": "7e02b8e0-9548-492e-9e42-8d5d6457d0b1", "creator_id": "", "guess": "human", "model_score": 0.2395, "style_score": 0.5, "combined_score": 0.31765, "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.", "status": "decided"}
{"timestamp": "2026-11-05T00:13:53+00:00", "content_id": "108b4001-4118-407a-bc16-7feeeea3e034", "creator_id": {"id": "x"}, "guess": "human", "model_score": 0.0492, "style_score": 0.5, "combined_score": 0.18444, "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.", "status": "decided"}
{"timestamp": "2026-11-05T00:13:54+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "6 per 1 minute"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP03, content_id `cbdabe0c-9448-48a7-bfce-cf37443793e1`.** A non-native English
speaker wrote a plain, careful paragraph about their first month in a new
country. The service scored it 0.805 on signal one and 0.515 on signal two
(combined 0.718) and told them it "shows patterns commonly associated with
AI-generated writing." Short, simple sentences and common vocabulary are
exactly what a careful second-language writer produces, and also what the
model signal reads as low-perplexity, machine-like text. The label's hedge
("does not prove that AI was used") doesn't help much: the writer is still
being told, about a deeply personal account, that it looks machine-made, and
the cause is who they are rather than anything they did. Five other human
texts (FP02, FP04, FP05, FP06, FP07) got the same label, but this is the one
where the error falls on a person for how they speak.


---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives | At most 2 of 10 of my own texts get `guess: "ai"`, in every trial | 1 of 10 `ai` (8 unsure, 1 human) | 1 of 10 | 1 of 10 | **MET** |
| 2. Score spread | Mean combined score of 5 AI texts at least 0.20 above 5 human texts | AI 0.706, human 0.533, gap **0.172** | 0.172 | 0.172 | **MISSED** (all 3) |
| 3. Label coverage | `human`, `unsure` and `ai` each appear at least once | all three appear (3 ai, 1 human, 2 unsure) | same | same | **MET** |
| 4. Appeal path | Appeal returns 200, logs `under_review`, keeps the original; unknown id returns 404 | 200 `under_review`, original kept, unknown id 404 | same | same | **MET** (3 manual trials; `run_eval.py` cannot drive an appeal) |
| 5. Bad input | Missing/empty/whitespace `text` returns 422; over 10,000 characters returns 413 | 0 of 4 correct | 0 of 4 | 0 of 4 | **MISSED** (all 3) |

Run: `python run_eval.py --label before`, output in
`results/run_2026-11-04_1756_before.md`. All three trials returned identical
scores for every input, so they confirmed stability but added no new
information: the model signal is deterministic here, and a 0.172 gap is the
same 0.172 each time. Criterion 2 is computed from the logged scores as
`0.7 * model_score + 0.3 * style_score`, since the eval report does not
include `combined_score`. For criterion 5 the first two bodies (no `text`,
empty `text`) show status `null` because the service answered with a non-JSON
error page and `run_eval.py` fails on `response.json()` before it records the
status code; the whitespace body got 200 and the 10,001-character body got 200.

**Real output for each criterion, trial 1 of `python run_eval.py --label before`.**
Produced by `run_eval.py::main` (the `results.append(...)` loop that posts each
body to `/submit`), written by `run_eval.py::write_report` to
`results/run_2026-11-04_1756_before.md`. Pasted unedited; trials 2 and 3 in that
file are identical. The `sent` field is truncated by `run_eval.py::describe`.

*Criterion 1. False positives* (scenario `my own writing`)

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5,
    "model_score": 0.8062,
    "style_score": 0.5608874019170043,
    "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
    "sent": "The tutorial is about GIMP which is an image editing application. It t"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.4635,
    "style_score": 0.4397760702021965,
    "label": "We cannot confidently determine whether this text was written by a person or AI.",
    "sent": "The formatting and design is great. I didn\u2019t see anything confusing. I"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.5751,
    "style_score": 0.45761994855822524,
    "label": "We cannot confidently determine whether this text was written by a person or AI.",
    "sent": "The author explains on the first page what GIMP tutorial is about. It "
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.5,
    "model_score": 0.221,
    "style_score": 0.4527990387582848,
    "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
    "sent": "Adding an image for the windows enable/disable settings would make it "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.5445,
    "style_score": 0.5503902496747589,
    "label": "We cannot confidently determine whether this text was written by a person or AI.",
    "sent": "The tutorial is about how a user can use Gmail and its email sorting f"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.456,
    "style_score": 0.5520677419595373,
    "label": "We cannot confidently determine whether this text was written by a person or AI.",
    "sent": "The author probably assumed that the readers need to know every bit of"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.3446,
    "style_score": 0.47024747632741204,
    "label": "We cannot confidently determine whether this text was written by a person or AI.",
    "sent": "Using high resolution images so the texts are more visible. Rephrasing"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.5824,
    "style_score": 0.523294654018869,
    "label": "We cannot confidently determine whether this text was written by a person or AI.",
    "sent": "The tutorial is about using youTube. The author explains how a user ca"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.4018,
    "style_score": 0.5335729453668189,
    "label": "We cannot confidently determine whether this text was written by a person or AI.",
    "sent": "The author does a good job on explaining each feature the app has. The"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.3353,
    "style_score": 0.4807926013898646,
    "label": "We cannot confidently determine whether this text was written by a person or AI.",
    "sent": "I didn\u2019t notice any redundancies. The intro does not mention anything "
  }
]
```

*Criterion 2. Score spread* (scenario `score spread`)

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5,
    "model_score": 0.7191,
    "style_score": 0.4975991026808101,
    "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
    "sent": "Artificial intelligence is transforming modern industries by improving"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5,
    "model_score": 0.9315,
    "style_score": 0.4887578749998101,
    "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
    "sent": "Climate change is one of the most significant challenges facing the wo"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5,
    "model_score": 0.8354,
    "style_score": 0.415785855065232,
    "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
    "sent": "Technology plays an important role in modern education. Online learnin"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5,
    "model_score": 0.8571,
    "style_score": 0.441374509052427,
    "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
    "sent": "Maintaining a healthy lifestyle requires a combination of regular phys"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.7009,
    "style_score": 0.4846153846153846,
    "label": "We cannot confidently determine whether this text was written by a person or AI.",
    "sent": "Cybersecurity has become increasingly important as organizations store"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5,
    "model_score": 0.8054,
    "style_score": 0.5275820271799756,
    "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
    "sent": "The tutorial is about GIMP which is an image editing application. It t"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.3686,
    "style_score": 0.3457109452053455,
    "label": "We cannot confidently determine whether this text was written by a person or AI.",
    "sent": "The formatting and design is great. I didn\u2019t see anything confusing. I"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.5311,
    "style_score": 0.5015531779209179,
    "label": "We cannot confidently determine whether this text was written by a person or AI.",
    "sent": "The tutorial is about how a user can use Gmail and its email sorting f"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.5741,
    "style_score": 0.47338000286720444,
    "label": "We cannot confidently determine whether this text was written by a person or AI.",
    "sent": "The tutorial is about using youTube. The author explains how a user ca"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.4999,
    "style_score": 0.558661052885839,
    "label": "We cannot confidently determine whether this text was written by a person or AI.",
    "sent": "I think the author assumed the users are beginner because the tutorial"
  }
]
```

*Criterion 3. Label coverage* (scenario `label coverage`)

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5,
    "model_score": 0.7374,
    "style_score": 0.4735877351967195,
    "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
    "sent": "Artificial intelligence is transforming modern industries by improving"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.5,
    "model_score": 0.2877,
    "style_score": 0.47117698959976834,
    "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
    "sent": "The author does well job on explaining the windows Modes. It would hav"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5,
    "model_score": 0.7485,
    "style_score": 0.4947435712431848,
    "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
    "sent": "I think the tutorial is good overall. Some parts are easy to understan"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.637,
    "style_score": 0.4468626430767404,
    "label": "We cannot confidently determine whether this text was written by a person or AI.",
    "sent": "The tutorial explains how people can use the application. I liked some"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5,
    "model_score": 0.8528,
    "style_score": 0.4223525045507832,
    "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
    "sent": "Technology has changed how people communicate with each other. Many pe"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.5122,
    "style_score": 0.4683027421096951,
    "label": "We cannot confidently determine whether this text was written by a person or AI.",
    "sent": "The author explains the topic clearly in most sections. However, I not"
  }
]
```

*Criterion 4. Appeal path* (scenario `appeal path`)

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.6227,
    "style_score": 0.34980844735229033,
    "label": "We cannot confidently determine whether this text was written by a person or AI.",
    "sent": "Technology allows people to communicate and share information quickly."
  }
]
```

*Criterion 4, manual test* (not produced by `run_eval.py`, which only posts to
`/submit`). I ran this by hand against the live service with a short Python
script using `urllib` to `POST /submit`, then `POST /appeal`, then `GET /log`.
Real responses, 2026-11-05 03:59 UTC:

```
SUBMIT 200
{"combined_score": 0.5408325342056871, "confidence": 0.5,
 "content_id": "0933ee38-fdfa-4cfc-a539-5b3ab2506937", "guess": "unsure",
 "label": "We cannot confidently determine whether this text was written by a person or AI.",
 "model_score": 0.6227, "style_score": 0.34980844735229033}

APPEAL (real content_id, reasoning given) 200
{"content_id": "0933ee38-fdfa-4cfc-a539-5b3ab2506937",
 "message": "Your appeal has been submitted and is under review.",
 "status": "under_review"}

APPEAL (content_id "does-not-exist") 404
{"error": "not_found", "message": "No submission found with that content_id."}
```

Audit log entries for that `content_id` afterwards (the original decision is
untouched; the appeal is a separate entry):

```json
{"combined_score": 0.5408325342056871, "content_id": "0933ee38-fdfa-4cfc-a539-5b3ab2506937", "creator_id": "eval_appeal", "guess": "unsure", "label": "We cannot confidently determine whether this text was written by a person or AI.", "model_score": 0.6227, "status": "decided", "style_score": 0.34980844735229033, "timestamp": "2026-11-05T03:59:28+00:00"}
{"content_id": "0933ee38-fdfa-4cfc-a539-5b3ab2506937", "creator_id": "eval_appeal", "event": "appeal", "reasoning": "I wrote this myself and believe the detector incorrectly classified it.", "status": "under_review", "timestamp": "2026-11-05T03:59:28+00:00"}
```

Repeated three times by hand (2026-11-05, creators `eval_appeal_run1` to `eval_appeal_run3`), each: submit, appeal with reasoning, appeal with an unknown id, then read the log for that `content_id`:

```
run 1: submit 200 unsure | appeal 200 under_review | unknown id 404 | log: decided, appeal(under_review)
run 2: submit 200 unsure | appeal 200 under_review | unknown id 404 | log: decided, appeal(under_review)
run 3: submit 200 unsure | appeal 200 under_review | unknown id 404 | log: decided, appeal(under_review)
```

Gap found while testing, outside what criterion 4 promises: `/appeal` also
returns 200 and logs `under_review` when `reasoning` is empty or missing (two
extra log entries with `"reasoning": ""`), and returns 404 rather than a 422
when `content_id` is missing. The criterion only requires 200 for a non-empty
reasoning, so it is met, but a blank appeal should be rejected.

*Criterion 5. Bad input* (scenario `bad input`)

```json
[
  {
    "status": null,
    "error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)",
    "sent": "{\"creator_id\": \"eval_missing_text\"}"
  },
  {
    "status": null,
    "error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)",
    "sent": "(empty text)"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5,
    "model_score": 0.7997,
    "style_score": 1.0,
    "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
    "sent": "   "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.5,
    "model_score": 0.9976,
    "style_score": 0.5,
    "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
    "sent": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  }
]
```


**Diagnoses**

Grouped by the stage that caused each failure: the route (`app.py::submit`), signal one (`detector.py::model_signal`), signal two (`stylometry.py::style_signal`), the combining rule (`scoring.py::combine_signals`, `0.70 * model + 0.30 * style`) and the label mapping (`scoring.py::score_to_label`, thresholds 0.35 and 0.65). Scores come from `results/attack_run_2026-11-04_1613.md` and `results/run_2026-11-04_1756_before.md`.

**1. The route: ten crashes and four accepted bad inputs (one problem).**
`app.py::submit` still has the starter body. It takes `payload.get("text", "")` and passes it straight to the detector without checking its type or length.

- *Ten attacks returned 500.* MF02, RQ01, RQ04, RQ08, RQ09 and RQ10 reach `detector.perplexity` with empty or tiny text, which raises `ValueError: Text is too short to score`. RQ03 (number), RQ05 (null) and RQ12 (nested object) pass a non-string to the tokenizer, which raises its own `ValueError`. RQ07 (JSON array) is truthy, so `or {}` doesn't replace it and `payload.get` raises `AttributeError`. The rate limiter's key function guards against this with `isinstance(payload, dict)`, but the route doesn't.
- *Accepted but should be rejected.* Whitespace-only text (MF01, and the eval's `"   "`) is scored and logged. The 10,001-character eval body and MF08 (60,000 characters) both got 200, because there is no length cap; the detector silently truncates at 400 tokens. RQ02 (no `creator_id`) and RQ06 (object `creator_id`) are logged as decisions, and RQ06 writes `{"id": "x"}` into `logs/audit.jsonl`.
- `confidence = 0.5` is hard-coded, so every response reports 0.5.
- *RQ11 is untested, not held.* Its 429 most likely came from the shared per-address bucket that RQ02 and RQ06 to RQ10 (no usable `creator_id`) had already filled, not from content-type handling.

This is criterion 5 missed in all three trials (0 of 4 correct).

**2. Signal one: false accusations, evasions and garbage scores (the largest problem).**
`model_signal` measures predictability, not authorship.

- *Plain human writing reads as AI.* FP02 to FP07 scored 0.74 to 0.88 on this signal and all six were labelled AI. FP03, a careful second-language writer, scored 0.8051 (combined 0.718). FP04 and FP05 are short declarative sentences in common words. FP06 (formal letter, 0.8814) and FP07 (deliberate repetition, 0.8816) are highest, since GPT-2 predicts a phrase it has just seen. This is the weakness the module docstring warns about, and it falls on writers with the least room to argue. One of my own ten texts (the GIMP review, 0.8062) was hit too.
- *Unpredictable text reads as human.* EV01 (typos) scored 0.1635, EV05 (heavy edit) 0.3212 and EV08 (two short sentences) 0.2452, so all three were labelled human. I expected the typos to work through signal two, but its score barely moved (0.4955); signal one fell, because misspellings and unusual voice are tokens the model didn't expect. EV08 is so short that a few surprising tokens dominate. I never submitted the unmodified base text, so I can't say how far each edit moved the score. The other evasions (EV02, 03, 04, 06, 07, 09) stayed in unsure.
- *Prompt injection worked only as noise.* PI02 scored 0.2044 and came back human, but no LLM reads the text. The `SYSTEM:` preamble is just odd tokens that raise perplexity. PI01 had the same base text with a different preamble and scored 0.4625, which suggests the tokens matter, not the instruction. PI03 to PI06 stayed unsure, and PI04's script tag never reached the label, which comes from a fixed table.
- *Garbage gets extreme scores.* Punctuation only (MF04, 0.0112) and control characters (MF03, 0.0) are maximally surprising, so they get a confident human. A repeated character (MF05, 0.9976) and emoji (MF06, 0.9969) are near-perfectly predictable, so they get a confident AI. Right-to-left text (MF07, 0.9064) was also called AI, which would accuse a writer in another script. I measured it: GPT-2's tokenizer breaks the Arabic into about one token per character (103 tokens for 105 characters, only 41 distinct), and its perplexity was 10.9, against 1.04 for MF05 (one token repeated 400 times) and 1.22 for MF06 (13 distinct tokens in 400). That is consistent with the model finding byte-level fragments and repeats easy to predict; I did not test the byte-level explanation directly.

**3. Signal two: no information about authorship, and maxed out by empty input.**
`style_signal` averages `1 / (1 + sentence_length_spread)` and `1 - type_token_ratio`. In the score-spread set the AI texts averaged 0.466 and the human texts 0.481, a gap of -0.016 against 0.253 on signal one. Input with no words (MF01, MF04, MF06, MF07) has spread 0 and vocabulary ratio 0, so the formula returns exactly 1.0, its most AI-like value. This is the designed blind spot: it measures shape, and empty input has none.

**4. The combining rule: signal two dilutes signal one.**
Criterion 2 needed a 0.20 gap and got 0.172 (AI 0.706, human 0.533) in all three trials. `0.70 * 0.253 - 0.30 * 0.016 = 0.172`, so the style signal can only shrink the gap. The GIMP false positive also hurts: without it the human mean is 0.486 and the gap is 0.219, which would pass. So the miss is one false positive plus a weak second signal. The rule also mishandles garbage: MF04's style score of 1.0 is outvoted by a model score of 0.0112, giving a combined 0.308 that reads as human. A 0.7/0.3 average never lets disagreement become "unsure"; the heavier signal just wins.

**5. The label mapping: correct as written, but the thresholds decide who is accused.**
`score_to_label` put every score in the right band and attacker text never reached a label (PI04 and PI05 held). The issue is the band edges. FP02 to FP07 combined to 0.68 to 0.79 and the AI attack EV10 to 0.895, so raising `AI_THRESHOLD` to about 0.80 would stop the six false accusations but push borderline AI cases (EV09 at 0.618, EV03 at 0.594) further from being caught. That trade lives in `config.py`, and right now it falls on the writer.

**What held:** the rate limiter (6 per minute per `creator_id`) let six flood requests through and returned 429 for the rest, each logged with `reason: rate_limited`. The appeal path met criterion 4 when tested by hand.

**Pattern:** the ten crashes are one missing validation step. The false positives, evasions and garbage scores all trace to signal one treating predictability as authorship, with signal two unable to correct it.

---

## The Improvement

**What I changed:** I added input validation at the top of `app.py::submit`, before any signal runs, plus `MAX_TEXT_CHARS = 10000` in `config.py`.

- A body that isn't a JSON object returns 422.
- `text` that isn't a string, or is empty or whitespace-only, returns 422.
- `text` over 10,000 characters returns 413.
- A missing or non-string `creator_id` falls back to the caller's address (the same fallback the rate limiter uses) instead of being logged as given.
- A `ValueError` from `detector.model_signal` (text with fewer than 3 tokens, like a single character) is caught and returned as 422.

Errors are JSON, so callers no longer get the Werkzeug HTML error page. The scoring code is unchanged.

**Which diagnosis pointed at it:** Diagnosis 1 (the route). All ten auto-BROKE attacks were 500s from `app.py::submit` handing unchecked input to the detector, and criterion 5 was missed 0 of 4 in all three trials. I picked it because it has no cost on the other side: rejecting a request that was never a real submission accuses no one. I did not touch the signals, the weights or the thresholds, so everything traced to signal one is unchanged on purpose.

### Attack Run — After

`python run_attacks.py --label after --set attack_set`, written to `results/attack_run_2026-11-04_2020_after.md`. Same 56 attacks, same marking rules as the before run, same layout, so the two can be compared row by row. Crashes are now HELD because the service rejects the input with a clean 422 or 413.

| Family | Attacks | Auto-BROKE | My BROKE | HELD | Total BROKE | Before | Which |
|---|---|---|---|---|---|---|---|
| evasion | 10 | 0 | 3 | 7 | 3 | 3 | EV01, EV05, EV08 (unchanged) |
| false_positive | 8 | 0 | 6 | 2 | 6 | 6 | FP02–FP07 (unchanged) |
| prompt_injection | 6 | 0 | 1 | 5 | 1 | 1 | PI02 (unchanged) |
| malformed | 20 | 0 | 5 | 15 | 5 | 17 | MF03–MF07. The 10 crashes, MF01, MF02, MF08, RQ02 and RQ06 are now HELD |
| flood_same_creator | 12 | 0 | 0 | 12 | 0 | 0 | first 6 returned 200, last 6 returned 429 (unchanged) |
| **Total** | **56** | **0** | **15** | **41** | **15** | **27** | |

Full output:

```
  [ 1/56] EV01    evasion           200   human    BROKE
  [ 2/56] EV02    evasion           200   unsure   HELD
  [ 3/56] EV03    evasion           200   unsure   HELD
  [ 4/56] EV04    evasion           200   unsure   HELD
  [ 5/56] EV05    evasion           200   human    BROKE
  [ 6/56] EV06    evasion           200   unsure   HELD
  [ 7/56] EV07    evasion           200   unsure   HELD
  [ 8/56] EV08    evasion           200   human    BROKE
  [ 9/56] EV09    evasion           200   unsure   HELD
  [10/56] EV10    evasion           200   ai       HELD
  [11/56] FP01    false_positive    200   unsure   HELD
  [12/56] FP02    false_positive    200   ai       BROKE
  [13/56] FP03    false_positive    200   ai       BROKE
  [14/56] FP04    false_positive    200   ai       BROKE
  [15/56] FP05    false_positive    200   ai       BROKE
  [16/56] FP06    false_positive    200   ai       BROKE
  [17/56] FP07    false_positive    200   ai       BROKE
  [18/56] FP08    false_positive    200   human    HELD
  [19/56] PI01    prompt_injection  200   unsure   HELD
  [20/56] PI02    prompt_injection  200   human    BROKE
  [21/56] PI03    prompt_injection  200   unsure   HELD
  [22/56] PI04    prompt_injection  200   unsure   HELD
  [23/56] PI05    prompt_injection  200   unsure   HELD
  [24/56] PI06    prompt_injection  200   unsure   HELD
  [25/56] MF01    malformed         422   —        HELD
  [26/56] MF02    malformed         422   —        HELD
  [27/56] MF03    malformed         200   human    BROKE
  [28/56] MF04    malformed         200   human    BROKE
  [29/56] MF05    malformed         200   ai       BROKE
  [30/56] MF06    malformed         200   ai       BROKE
  [31/56] MF07    malformed         200   ai       BROKE
  [32/56] MF08    malformed         413   —        HELD
  [33/56] RQ01    malformed         422   —        HELD
  [34/56] RQ02    malformed         200   human    HELD
  [35/56] RQ03    malformed         422   —        HELD
  [36/56] RQ04    malformed         422   —        HELD
  [37/56] RQ05    malformed         422   —        HELD
  [38/56] RQ06    malformed         200   human    HELD
  [39/56] RQ07    malformed         422   —        HELD
  [40/56] RQ08    malformed         422   —        HELD
  [41/56] RQ09    malformed         422   —        HELD
  [42/56] RQ10    malformed         422   —        HELD
  [43/56] RQ11    malformed         429   —        HELD
  [44/56] RQ12    malformed         422   —        HELD
  [45/56] FL01_01 flood_same_creator 200   human    HELD
  [46/56] FL01_02 flood_same_creator 200   human    HELD
  [47/56] FL01_03 flood_same_creator 200   human    HELD
  [48/56] FL01_04 flood_same_creator 200   human    HELD
  [49/56] FL01_05 flood_same_creator 200   human    HELD
  [50/56] FL01_06 flood_same_creator 200   human    HELD
  [51/56] FL01_07 flood_same_creator 429   —        HELD
  [52/56] FL01_08 flood_same_creator 429   —        HELD
  [53/56] FL01_09 flood_same_creator 429   —        HELD
  [54/56] FL01_10 flood_same_creator 429   —        HELD
  [55/56] FL01_11 flood_same_creator 429   —        HELD
  [56/56] FL01_12 flood_same_creator 429   —        HELD
============================================================
  auto-marked BROKE: 0
  judged by me:      56  (41 HELD, 15 BROKE)
  final:             15 BROKE, 41 HELD
============================================================
```

Criterion 5, `python run_eval.py --label after` (`results/run_2026-11-04_2020_after.md`): **4 of 4 correct in all three trials** (missing `text` 422, empty 422, whitespace 422, 10,001 characters 413), up from 0 of 4. Criteria 1 and 3 are unchanged (met), criterion 2 is unchanged (0.172 gap, still missed). The same results held in all three trials.

**Did it help, and how do I know:** It fixed what it targeted and nothing else. Crashes went from 10 to 0, criterion 5 went from missed to met, and the BROKE count dropped from 27 to 15. The 15 that remain are all scores from the signals, and the scores are identical to the before run (for example FP03 is still 0.8051 on the model signal), which is evidence the validation did not change the scoring. That also confirms the diagnosis: the crashes were one missing check, and what's left is signal one reading predictability as authorship.

There is a trade, but it is small. The 10,000-character cap rejects long documents that were previously scored (on only their first 400 tokens), and a writer who sends a missing `creator_id` is now logged under their IP address, which can be shared by many people and share a rate-limit bucket.

Two things this did not fix:
- MF03 (control characters), MF04 (punctuation only), MF05 (one long word), MF06 (emoji) and MF07 (right-to-left script) are still scored with a confident label. They are non-empty strings, so validation passes them. I chose not to add a minimum word count because it would also reject FP08, which is genuine human text.
- RQ11 still returns 429, not a result. It shares the address bucket with the other requests that have no `creator_id`, so it still never tested content-type handling. A malformed body without a `creator_id` is not exempt from the limiter.

---

## What's Still Broken

After the input-validation fix, 15 of 56 attacks still get through and one criterion (2) is still missed. Everything left comes from the scoring, not the route. I stopped here because the assignment asks for one improvement and I picked the one with no trade on the other side. Each fix below moves a threshold or a weight, and I haven't tested any of them across three trials, so I haven't changed them.

**Human writing called AI: FP02–FP07 (6 attacks).**
These combine to 0.68 to 0.79. What I'd do: raise `AI_THRESHOLD` in `config.py` from 0.65 to about 0.80. The cost is on the other side: in my score-spread set four of the five clear-AI texts combine to 0.65 to 0.80 (0.653, 0.710, 0.732, 0.799), so they would drop from "ai" to "unsure". Only the most extreme AI text, like EV10 at 0.895, would still be labelled AI. I didn't do it because that is a decision about how much missed AI I accept, and I wanted to make it deliberately.

**Evasions that read as human: EV01, EV05, EV08 (3 attacks), and PI02.**
Typos, a heavy edit, very short text and an odd preamble all lower signal one, because the model finds unusual tokens surprising. There is no cheap fix. For EV08 (two short sentences) I'd stop the service from giving a confident "human" or "ai" label to text under a minimum length and return "unsure" instead. For typos I'd need a signal that is not perplexity, which is more work than this unit allowed. PI02 isn't a real injection (nothing reads instructions); it's the same noise as the typos, so it is fixed by the same changes.

**Garbage with a confident label: MF03–MF07 (5 attacks).**
These are non-empty strings, so validation lets them through. What I'd do: reject text with fewer than 2 words or mostly non-letter characters, which would catch MF03 to MF06. It would not catch MF07 (right-to-left text), because those are letters; its tokens are fragmented and repetitive (103 tokens, 41 distinct, perplexity 10.9), so only a change to the detector would fix it. I held off on a word-count rule at your direction and because a stricter rule would start rejecting short genuine text like FP08.

**Criterion 2 (score spread) still missed: 0.172 against 0.20, in all three trials.**
Signal two separates the groups by -0.016, so it only dilutes signal one's 0.253 gap. What I'd do: cut the style weight, for example to 0.85 / 0.15 in `config.py`. By my arithmetic that gives a gap of about 0.213, which would pass, but I haven't run it. It would also shift every other score and the label bands (criterion 3), so it needs a full re-run of the eval before I trust it. It also leaves the six false positives untouched, because those come from signal one.

**Smaller items**
- *RQ11 was never tested.* It still returns 429 from the shared address bucket, so it needs a re-run on its own.
- *Appeals accept an empty `reasoning`.* Criterion 4 is met as written, but `/appeal` should return 422 for a blank reason and for a missing `content_id`. I found this while testing and haven't fixed it.
- *`confidence` is hard-coded to 0.5.* Every response reports it, so it carries no information.
- *Criterion 4 was tested once by hand, not across three trials,* because `run_eval.py` can't drive an appeal.

**The trade I'd make if this ran for real:**
I'd go toward fewer wrong accusations: raise the AI threshold so "ai" is reserved for the clearest cases, and keep the appeal path. The cost of that falls on the site and on readers and honest writers who compete with undetected AI text, and I'd accept that over making a second-language writer like FP03 pay for a wrong label about their own work.

---

# Unit 9 — Capstone

Everything above this line is Units 7 and 8 and is left as submitted. Everything below is new in Unit 9. Entries marked `TBD` are filled in only after the system has actually been run and measured; nothing in those places is an estimate.

---

## Unit 9 — What This Extends

**System extended:** Provenance Guard, the same repository and the same service built in Units 7 and 8. It is a Flask web service that scores a piece of text two ways (GPT-2 perplexity, and a stylometry signal), combines the two scores, returns a `human` / `unsure` / `ai` label, writes each decision to `logs/audit.jsonl`, and accepts appeals at `/appeal`. It is not being rewritten, and its detection logic is not being changed.

**What is new:** an operational layer around the existing service, so that its behavior can be seen after the fact:

- A per-request **ops log** (`logs/requests.jsonl`, one JSON object per line). It records a timestamp, a request ID, the route, the status code, what came in (text length and a short hash, not the raw text), what came out, total duration, the time spent in each stage (GPT-2, stylometry, scoring, audit write) and CPU time. Rejected and failed requests get lines too.
- A **request ID** on every response, so a response can be matched to its log line.
- A documented local **run path** (`waitress`) with a `RUNNING.md` that has been followed from a clean checkout.
- A small `summarize_log.py` that reads the ops log back and reports counts, error rate and latency percentiles.
- A measured **cost per run**.

The Unit 7/8 audit log stays the record of *decisions*. The ops log is the record of *requests*. They are separate files on purpose, so the audit log's shape does not change.

---

## Unit 9 — The Shape

**Shape A — Deploy and instrument.** The extension is the operational layer described above: the run path, the instrumentation, and the numbers that come out of it. Provenance Guard has only ever run from my editor and Flask's development server. This unit puts it behind a documented start command and makes its behavior measurable.

**Deployment path: Path B, local with logs.** The system carries a local GPT-2 model (about 550 MB on disk, loaded into memory), which does not fit a free 512 MB hosted tier. No cloud deployment is attempted.

**Out of scope** (considered and deliberately not done):

- **No cloud or hosted deployment**, and no containers.
- **No changes to the detection logic.** The signals, the weights (0.70 / 0.30) and the label thresholds (0.35 / 0.65) stay as they were at the end of Unit 8. One Unit 9 criterion checks that scores did not change.
- **No metrics server or dashboard.** No `/metrics` endpoint and no Prometheus. Counts and latency come from reading the ops log back with `summarize_log.py`.
- **No fixes for the Unit 8 leftovers** (the false positives, `confidence` hard-coded to 0.5, the empty-`reasoning` appeal). Those belong to Unit 8's "What's Still Broken", and the improvements this unit are chosen from this unit's own diagnosis.

**Stretch items I am declaring before building them** (committed before any of them are built):

1. **A second measured improvement** (+2): a second change drawn from the diagnosis, with a third run log in the same table format and a statement of whether it helped.
2. **A latency breakdown** (+1): where the time goes across the stages of one run, measured, with the numbers here and a sentence on which stage dominates.
3. **A load observation** (+1): the service run at roughly ten times its normal rate, with a report on what changed.

Not attempting: "both run paths" (it needs a hosted deployment).

---

## Unit 9 — Running It

**Path B — local with logs.** `RUNNING.md` is the authoritative run path; this section is a summary and will be completed once the instructions have been tested from a clean checkout.

| Item | Value |
|---|---|
| Python | 3.13.13 in the project's `.venv` (the starter supports 3.11, 3.12 and 3.13, not 3.14) |
| Dependencies | pinned with lower and upper bounds in `requirements.txt` (Flask, Flask-Limiter, requests, transformers, torch, certifi); `waitress` to be added |
| Model | `gpt2`, about 550 MB, downloaded once into the Hugging Face cache |
| Start command | TBD (`waitress`; fallback `python app.py` with `AI201_DEBUG=0`) |
| Clean-checkout test | TBD (what I had to fix in `RUNNING.md` is recorded here) |

---

## Unit 9 — Instrumentation

TBD. This section will hold the ops-log field list and at least ten real entries pasted as text, including at least one rejected or failed request.

---

## Unit 9 — What It Costs

TBD. This section will hold the measured per-request cost (CPU seconds and wall seconds, averaged over ten runs), how it was measured, and the hundred-a-day arithmetic.

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
