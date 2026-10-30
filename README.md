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

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

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
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit   -H "Content-Type: application/json"   -d '{"text": "Artificial intelligence is changing many industries. Businesses use these systems to automate repetitive tasks and improve efficiency. Organizations must consider accuracy, privacy, and responsible use.", "creator_id": "test-user"}'
```

```json
{
  "confidence": 0.5,
  "content_id": "fa779b28-78e5-44f9-ab08-3b8dde384e9d",
  "guess": "model_signal",
  "label": "pending",
  "model_score": 0.538,
  "style_score": 0.5
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": null,
      "content_id": "c9fbedea-c5f6-43ad-8bff-f7eac8a73d21",
      "creator_id": "test-user",
      "guess": "model_signal",
      "label": "pending",
      "model_score": 0.6007,
      "status": "decided",
      "style_score": 0.5,
      "timestamp": "2026-10-29T07:26:41+00:00"
    },
    {
      "combined_score": null,
      "content_id": "49ade757-b338-4329-a23c-120354a4bafb",
      "creator_id": "test-user",
      "guess": "model_signal",
      "label": "pending",
      "model_score": 0.733,
      "status": "decided",
      "style_score": 0.5,
      "timestamp": "2026-10-29T07:33:38+00:00"
    },
    {
      "combined_score": null,
      "content_id": "fa779b28-78e5-44f9-ab08-3b8dde384e9d",
      "creator_id": "test-user",
      "guess": "model_signal",
      "label": "pending",
      "model_score": 0.538,
      "status": "decided",
      "style_score": 0.5,
      "timestamp": "2026-10-29T08:02:01+00:00"
    }
  ]
}
```

```json
{
  "count": 1,
  "entries": [
    {
      "combined_score": 0.70688,
      "content_id": "e48f16ad-97ce-4afb-8ba4-84580bf1707d",
      "creator_id": "test_user",
      "guess": "model_signal",
      "label": "pending",
      "model_score": 0.7884,
      "status": "decided",
      "style_score": 0.5166666666666666,
      "timestamp": "2026-10-30T07:07:41+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

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



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



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
