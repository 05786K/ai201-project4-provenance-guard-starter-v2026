# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 17:53
- Auto-marked BROKE (5xx, crash, no response): **10**
- Left for you to judge: **46** → judged: **29 HELD, 17 BROKE**
- Final totals: **27 BROKE, 29 HELD**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `5dc8b296-b6dd-4bbd-8cc7-082b0883a6ee` | human | 0.500 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `524cde0c-183c-44ac-9782-13ce7c6f8aa2` | unsure | 0.500 | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `f0e57feb-16fb-4e20-8125-818eb115c658` | unsure | 0.500 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `6db5c08c-5597-4870-8bc0-6aa70b8f7049` | unsure | 0.500 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `5c1e21f4-3134-44c4-8d81-c9ac81f6404c` | human | 0.500 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `489cc241-337a-4075-a2eb-ac5b6332a2db` | unsure | 0.500 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | `ba0ab333-22e1-4cfe-8999-5e2924cc639c` | unsure | 0.500 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `975b39e0-5d9b-40c8-9a08-f4958d79384d` | human | 0.500 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `c98cc356-36ad-4e22-8b21-387b7a4acc71` | unsure | 0.500 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `4c0258c5-c72e-48fc-a1f9-e3e771f64649` | ai | 0.500 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `646239e4-120a-4092-9cf9-6f4d89f98d7c` | unsure | 0.500 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `51071729-d750-44e4-8ef4-55499ebe9e67` | ai | 0.500 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `f406f22b-e197-4a70-b739-7ca1155412ec` | ai | 0.500 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `6e849807-b82e-45dd-baf1-283d81bcaab4` | ai | 0.500 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `98c33b1f-6895-49e1-8c46-2952e616a1db` | ai | 0.500 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `d72a2ba3-de06-4155-9531-fef508a970e5` | ai | 0.500 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `98c7477b-3e7a-44e3-b7a6-43a9c6ebfd4a` | ai | 0.500 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `572d2b07-77e1-43d2-83ce-06a311007650` | human | 0.500 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `d0db0a09-8938-4d34-940c-840c5d85c6dd` | unsure | 0.500 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `edc9a6ec-666c-4e9d-8ce2-f90c181ee2d3` | human | 0.500 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `052da94c-d7e0-439d-8d41-2abbd577c529` | unsure | 0.500 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `65a628df-6a10-4c7e-92ad-3de87116e77d` | unsure | 0.500 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `8e0395fa-9ef2-4053-ab14-d0e4cf51d6ac` | unsure | 0.500 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `a24f28be-5ed8-4476-a343-f56e8d9b004e` | unsure | 0.500 | HELD |
| MF01 | malformed | text is only whitespace | 200 | `d4f35af2-b62a-409e-8c1e-b9a3e697d520` | unsure | 0.500 | HELD |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `dbf3070d-f1ee-4b1b-9e8c-9658c9541129` | human | 0.500 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `b5280340-b476-46b3-b011-19fb25bc49b4` | human | 0.500 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `ffe6d64e-411a-4b31-91cb-4785b67fa8d8` | ai | 0.500 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `09f0ed4e-a054-4fb1-a122-0251508261ee` | ai | 0.500 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `ba3880e0-00fe-4706-89df-d60a364a2b89` | ai | 0.500 | BROKE |
| MF08 | malformed | text is 60,000 characters | 200 | `d9906696-01f5-439b-a7e0-27ca62cf4b97` | ai | 0.500 | HELD |
| RQ01 | malformed | no text field at all | 500 | `—` | — | — | BROKE |
| RQ02 | malformed | no creator_id | 200 | `ddc7d874-e2c8-420b-9e8a-997d974c329d` | human | 0.500 | BROKE |
| RQ03 | malformed | text is a number | 500 | `—` | — | — | BROKE |
| RQ04 | malformed | text is a list | 500 | `—` | — | — | BROKE |
| RQ05 | malformed | text is null | 500 | `—` | — | — | BROKE |
| RQ06 | malformed | creator_id is an object | 200 | `070dee49-9ed3-40b1-b9bc-a66e26630472` | human | 0.500 | BROKE |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 500 | `—` | — | — | BROKE |
| RQ09 | malformed | body is empty | 500 | `—` | — | — | BROKE |
| RQ10 | malformed | body is form-encoded, not JSON | 500 | `—` | — | — | BROKE |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 500 | `—` | — | — | BROKE |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `adabecd9-26d6-444e-a00f-f0cab24db502` | human | 0.500 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `986e0ac0-8c82-4416-9c36-d6c473892cff` | human | 0.500 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7440460a-96b6-47b2-a003-adced2d05dd6` | human | 0.500 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c5bd392f-d830-4515-9dba-6e01a7d03035` | human | 0.500 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a5340b2c-7afa-444b-8561-9b73b86fb7bc` | human | 0.500 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f6d437d7-9cac-45c8-80ed-c4b32c7329f5` | human | 0.500 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 10 | 10 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "5dc8b296-b6dd-4bbd-8cc7-082b0883a6ee",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.1635,
  "style_score": 0.4954668754756913,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "524cde0c-183c-44ac-9782-13ce7c6f8aa2",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5943,
  "style_score": 0.35830377692563603,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": "HELD"
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "f0e57feb-16fb-4e20-8125-818eb115c658",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6662,
  "style_score": 0.4265987253847264,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": "HELD"
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "6db5c08c-5597-4870-8bc0-6aa70b8f7049",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6114,
  "style_score": 0.4898367746903978,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": "HELD"
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "5c1e21f4-3134-44c4-8d81-c9ac81f6404c",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.3212,
  "style_score": 0.4143144609464353,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "489cc241-337a-4075-a2eb-ac5b6332a2db",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5727,
  "style_score": 0.35373571642174273,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": "HELD"
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "ba0ab333-22e1-4cfe-8999-5e2924cc639c",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5862,
  "style_score": 0.6134020618556701,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": "HELD"
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "975b39e0-5d9b-40c8-9a08-f4958d79384d",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.2452,
  "style_score": 0.3897593953942288,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "c98cc356-36ad-4e22-8b21-387b7a4acc71",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.7042,
  "style_score": 0.4172836464507392,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": "HELD"
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "4c0258c5-c72e-48fc-a1f9-e3e771f64649",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.9792,
  "style_score": 0.6984481156837643,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": "HELD"
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "646239e4-120a-4092-9cf9-6f4d89f98d7c",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6175,
  "style_score": 0.4886832368451833,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": "HELD"
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "51071729-d750-44e4-8ef4-55499ebe9e67",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.7387,
  "style_score": 0.5478491020831722,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "f406f22b-e197-4a70-b739-7ca1155412ec",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.8051,
  "style_score": 0.5150066988642605,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "6e849807-b82e-45dd-baf1-283d81bcaab4",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.8329,
  "style_score": 0.4614384854953659,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "98c33b1f-6895-49e1-8c46-2952e616a1db",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.8005,
  "style_score": 0.5987200437327835,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "d72a2ba3-de06-4155-9531-fef508a970e5",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.8814,
  "style_score": 0.4619408908912053,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "98c7477b-3e7a-44e3-b7a6-43a9c6ebfd4a",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.8816,
  "style_score": 0.5600513751364047,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "572d2b07-77e1-43d2-83ce-06a311007650",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.3223,
  "style_score": 0.34891526037401893,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "d0db0a09-8938-4d34-940c-840c5d85c6dd",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.4625,
  "style_score": 0.3340572490327385,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": "HELD"
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "edc9a6ec-666c-4e9d-8ce2-f90c181ee2d3",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.2044,
  "style_score": 0.32491589015512873,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": "BROKE"
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "052da94c-d7e0-439d-8d41-2abbd577c529",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5943,
  "style_score": 0.41774043445300435,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": "HELD"
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "65a628df-6a10-4c7e-92ad-3de87116e77d",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.4998,
  "style_score": 0.42661268712330636,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": "HELD"
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "8e0395fa-9ef2-4053-ab14-d0e4cf51d6ac",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6401,
  "style_score": 0.35647804615814627,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": "HELD"
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "a24f28be-5ed8-4476-a343-f56e8d9b004e",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5583,
  "style_score": 0.4919348976712607,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": "HELD"
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 200,
  "content_id": "d4f35af2-b62a-409e-8c1e-b9a3e697d520",
  "creator_id": "attacker_MF01",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.2053,
  "style_score": 1.0,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": "HELD"
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "dbf3070d-f1ee-4b1b-9e8c-9658c9541129",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": "BROKE"
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "b5280340-b476-46b3-b011-19fb25bc49b4",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": "BROKE"
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "ffe6d64e-411a-4b31-91cb-4785b67fa8d8",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": "BROKE"
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "09f0ed4e-a054-4fb1-a122-0251508261ee",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": "BROKE"
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "ba3880e0-00fe-4706-89df-d60a364a2b89",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": "BROKE"
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "d9906696-01f5-439b-a7e0-27ca62cf4b97",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.9876,
  "style_score": 0.8468696302321063,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": "HELD"
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "ddc7d874-e2c8-420b-9e8a-997d974c329d",
  "creator_id": null,
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.2395,
  "style_score": 0.5,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": "BROKE"
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: text input must be of type `str` (single example), `list[str]` (batch or single pretokenized example) or `list[list[str]]` (batch of pret",
  "verdict": "BROKE"
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: You need to specify either `text` or `text_target`.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&amp;",
  "verdict": "BROKE"
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "070dee49-9ed3-40b1-b9bc-a66e26630472",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0492,
  "style_score": 0.5,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": "BROKE"
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 500,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>AttributeError: &#39;list&#39; object has no attribute &#39;get&#39;\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes",
  "verdict": "BROKE"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 500,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 500,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 500,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: text input must be of type `str` (single example), `list[str]` (batch or single pretokenized example) or `list[list[str]]` (batch of pret",
  "verdict": "BROKE"
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "adabecd9-26d6-444e-a00f-f0cab24db502",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "986e0ac0-8c82-4416-9c36-d6c473892cff",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "7440460a-96b6-47b2-a003-adced2d05dd6",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "c5bd392f-d830-4515-9dba-6e01a7d03035",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "a5340b2c-7afa-444b-8561-9b73b86fb7bc",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "f6d437d7-9cac-45c8-80ed-c4b32c7329f5",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```
