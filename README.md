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



<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



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
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
