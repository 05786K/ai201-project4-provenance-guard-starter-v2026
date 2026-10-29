# Milestone 1 — Trace a Submission

## 1. Submission Path

1. **API (`app.py`)** — Receives the submission and validates the request.
2. **Detector (`detector.py`)** — Uses a local language model to measure text predictability and returns an AI-likeness score.
3. **Stylometry (`stylometry.py`)** — Measures sentence-length variation, vocabulary diversity, and punctuation density.
4. **Scoring (`scoring.py`)** — Combines the two signals into one score.
5. **Confidence logic** — Estimates how reliable the assessment is; agreement between signals does not prove authorship.
6. **Labeling** — Applies decision thresholds to produce a reader-friendly label.
7. **Response and appeal** — Returns the assessment, explanation, and a way for the writer to challenge it.

## 2. The Two Signals

### Signal 1: Model signal (`detector.py`)

- **Measures:** Perplexity—how predictable the text is to a local language model—converted to a score from `0.0` to `1.0`.
- **Why it may differ:** AI-generated text may be more predictable to a language model than human writing.
- **Blind spot:** Plain, predictable human writing may score as AI-like, while unusual or complex AI writing may score as human-like. Predictability does not prove authorship.
- **Direction and caveat:** Higher means more AI-like according to this heuristic, not a calibrated probability of AI authorship. The code uses a logistic transformation with a midpoint of `45.0`.

### Signal 2: Style signal (`stylometry.py`)

- **Measures:** Sentence-length spread, type-token ratio (vocabulary diversity), and punctuation density. These functions are currently stubs and will be implemented later.
- **Why it may differ:** AI writing may have more consistent sentence lengths and more predictable vocabulary patterns, while human writing may vary more.
- **Blind spot:** It cannot understand meaning or determine authorship. Typos, sentence splitting, or inserted quotations can change the measurements without changing who wrote the text.
- **Direction:** The final style score must use the same direction as the detector: higher means more AI-like.

## 3. False-Positive Scenario

A real poet submits an original poem written in plain, predictable language. The detector may mistake that predictability for AI-like writing, and the style signal may also misread the poem's patterns.

- **Hypothetical combined score:** `0.80`.
- **Hypothetical label:** `Potentially AI-generated`.
- **Impact:** The writer is falsely suspected of using AI.
- **Remedy:** The writer can submit an appeal for human review.

**Design rule:** A model prediction must not be treated as proof of cheating. Signal agreement alone does not guarantee correctness.

## 4. Endpoint Contracts

These are proposed contracts; confirm them against the starter code before implementation.

### Endpoint 1: `POST /assessments`

**Request fields**

| Field | Type | Required | Meaning |
|---|---|---|---|
| `text` | string | Yes | Text to assess; must not be empty and must meet the configured length limit. |
| `submission_id` | string or `null` | No | Optional ID from the writing platform. |

Example request:

```json
{
  "text": "My original poem",
  "submission_id": "submission_123"
}
```

**Response fields**

| Field | Type | Meaning |
|---|---|---|
| `assessment_id` | string | Unique ID for this assessment. |
| `submission_id` | string or `null` | Caller-provided ID, if supplied. |
| `score` | number from 0 to 1 | Combined score; higher means more AI-like. |
| `confidence` | number from 0 to 1 | Confidence estimate, defined separately from the score. |
| `label` | string | Reader-facing result based on documented thresholds. |
| `explanation` | string | Plain-language explanation and limitations. |
| `signals.detector` | number from 0 to 1 | Detector signal. |
| `signals.stylometry` | number from 0 to 1 | Stylometry signal. |
| `appeal_available` | boolean | Whether the writer can appeal. |

Example response (illustrative values):

```json
{
  "assessment_id": "pg_001",
  "submission_id": "submission_123",
  "score": 0.42,
  "confidence": 0.35,
  "label": "Insufficient evidence",
  "explanation": "The available signals do not support a reliable conclusion.",
  "signals": {
    "detector": 0.48,
    "stylometry": 0.36
  },
  "appeal_available": true
}
```

### Endpoint 2: `POST /assessments/{assessment_id}/appeals`

**Path parameter**

| Field | Type | Required | Meaning |
|---|---|---|---|
| `assessment_id` | string | Yes | ID of the assessment being challenged. |

**Request fields**

| Field | Type | Required | Meaning |
|---|---|---|---|
| `reason` | string | Yes | Writer's reason for challenging the result; must not be empty. |

Example request:

```json
{
  "reason": "I wrote this poem myself."
}
```

**Response fields**

| Field | Type | Meaning |
|---|---|---|
| `appeal_id` | string | Unique ID for the appeal. |
| `assessment_id` | string | Assessment being challenged. |
| `status` | string | Initially `pending_review`. |
| `message` | string | Confirmation that the appeal was received. |

Example response:

```json
{
  "appeal_id": "appeal_001",
  "assessment_id": "pg_001",
  "status": "pending_review",
  "message": "Your appeal has been received for review."
}
```