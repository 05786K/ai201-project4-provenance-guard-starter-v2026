# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 20:20
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `9b8cdb78-1bf9-4e08-8b2f-89464791342a` | human | 0.500 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c73b069b-3df5-4e4b-bbe0-1f98a5a4da75` | unsure | 0.500 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `965e8705-da04-4a08-a658-04e7fadd1af4` | unsure | 0.500 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c41bbe49-ac5a-4391-9a67-0d3292621eec` | unsure | 0.500 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c8e5a9e9-e0ec-401e-ab2c-8985918050dc` | human | 0.500 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `e85f7ea7-5ce8-4ef5-85ea-d1c32d975710` | unsure | 0.500 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `7394e4a7-a18e-4149-8f90-002f31955999` | unsure | 0.500 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `1a225eed-172c-4441-8203-0f9a5886c338` | human | 0.500 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `2e350bf0-7cee-45b2-8b24-9fda2c2c8575` | unsure | 0.500 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `0a4e8076-f3ca-4d80-9bed-93141ddae218` | ai | 0.500 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `f3d191d8-2748-4d27-a1b5-23f18af9e35e` | unsure | 0.500 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `40c2c16f-aa0d-4a5c-8467-f875d293a692` | ai | 0.500 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `bbd838f2-7117-4030-8212-d5df01325774` | ai | 0.500 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `7dc83e40-ad79-4e37-8743-adce53f316ec` | ai | 0.500 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `ea6e1865-7e39-4076-aac9-03c4dcbb0154` | ai | 0.500 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `94d638c7-7bfb-4e84-a8e7-b30d64c2d6d5` | ai | 0.500 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `8dd0b825-0d53-478b-8f9f-4ed7863ef6ef` | ai | 0.500 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `5cd874a4-aebe-442b-93c7-bbdcc0b3b35b` | human | 0.500 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `5ad2042b-fce4-46ad-a513-172d841d814d` | unsure | 0.500 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `ac41ad4b-3fb6-4a2f-80e0-9b2d7f2777e3` | human | 0.500 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `48cbdd6c-1b0e-4ad5-bef4-a60259e53c2a` | unsure | 0.500 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `a8edf0e0-9326-4c65-8c4e-0e7d744d0b5c` | unsure | 0.500 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `ab821dd5-54ca-4e3c-98ff-90bac2dc07cb` | unsure | 0.500 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `dd778737-657f-4ac5-bebc-0e3cce36f0f7` | unsure | 0.500 |  |
| MF01 | malformed | text is only whitespace | 422 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 422 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `e0b82378-f4e7-4a69-a81a-e2670d4dfe68` | human | 0.500 |  |
| MF04 | malformed | text is only punctuation | 200 | `589c74aa-a19b-46ae-80fa-e7ae62bbb76c` | human | 0.500 |  |
| MF05 | malformed | text is a very long single word | 200 | `99085f89-538b-40c1-8727-11179eb702a7` | ai | 0.500 |  |
| MF06 | malformed | text is emoji only | 200 | `d1f96eda-b8f9-472d-ab06-bd5bf9cb1828` | ai | 0.500 |  |
| MF07 | malformed | text is right-to-left script | 200 | `08306d28-ea80-4c95-bd64-e10c34068c9d` | ai | 0.500 |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 422 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `58b2cdf2-3338-4f6b-954c-9d9443758920` | human | 0.500 |  |
| RQ03 | malformed | text is a number | 422 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 422 | `—` | — | — |  |
| RQ05 | malformed | text is null | 422 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `1e9fbb99-8826-4963-b1fc-38c4ee7e2ab6` | human | 0.500 |  |
| RQ07 | malformed | body is a JSON array, not an object | 422 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 422 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 422 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 422 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 422 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1c914ae3-9cf3-4c58-a534-7200b1b2aff0` | human | 0.500 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `96c88071-f933-4ba0-a4cc-1fe0f62b62ae` | human | 0.500 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `772dc55d-c6ed-42a1-9039-7660429d0075` | human | 0.500 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7ec73169-9191-4d8b-8ec0-16fe4cf45e5b` | human | 0.500 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2ce16b7d-a32e-4d77-a10c-a08dbc8bc637` | human | 0.500 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4c72f504-0e23-48d3-b820-325607f3e8b5` | human | 0.500 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
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
  "content_id": "9b8cdb78-1bf9-4e08-8b2f-89464791342a",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.1635,
  "style_score": 0.4954668754756913,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "c73b069b-3df5-4e4b-bbe0-1f98a5a4da75",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5943,
  "style_score": 0.35830377692563603,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "965e8705-da04-4a08-a658-04e7fadd1af4",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6662,
  "style_score": 0.4265987253847264,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "c41bbe49-ac5a-4391-9a67-0d3292621eec",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6114,
  "style_score": 0.4898367746903978,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "c8e5a9e9-e0ec-401e-ab2c-8985918050dc",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.3212,
  "style_score": 0.4143144609464353,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "e85f7ea7-5ce8-4ef5-85ea-d1c32d975710",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5727,
  "style_score": 0.35373571642174273,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "7394e4a7-a18e-4149-8f90-002f31955999",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5862,
  "style_score": 0.6134020618556701,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "1a225eed-172c-4441-8203-0f9a5886c338",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.2452,
  "style_score": 0.3897593953942288,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "2e350bf0-7cee-45b2-8b24-9fda2c2c8575",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.7042,
  "style_score": 0.4172836464507392,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "0a4e8076-f3ca-4d80-9bed-93141ddae218",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.9792,
  "style_score": 0.6984481156837643,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "f3d191d8-2748-4d27-a1b5-23f18af9e35e",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6175,
  "style_score": 0.4886832368451833,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "40c2c16f-aa0d-4a5c-8467-f875d293a692",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.7387,
  "style_score": 0.5478491020831722,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "bbd838f2-7117-4030-8212-d5df01325774",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.8051,
  "style_score": 0.5150066988642605,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "7dc83e40-ad79-4e37-8743-adce53f316ec",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.8329,
  "style_score": 0.4614384854953659,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "ea6e1865-7e39-4076-aac9-03c4dcbb0154",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.8005,
  "style_score": 0.5987200437327835,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "94d638c7-7bfb-4e84-a8e7-b30d64c2d6d5",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.8814,
  "style_score": 0.4619408908912053,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "8dd0b825-0d53-478b-8f9f-4ed7863ef6ef",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.8816,
  "style_score": 0.5600513751364047,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "5cd874a4-aebe-442b-93c7-bbdcc0b3b35b",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.3223,
  "style_score": 0.34891526037401893,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "5ad2042b-fce4-46ad-a513-172d841d814d",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.4625,
  "style_score": 0.3340572490327385,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "ac41ad4b-3fb6-4a2f-80e0-9b2d7f2777e3",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.2044,
  "style_score": 0.32491589015512873,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "48cbdd6c-1b0e-4ad5-bef4-a60259e53c2a",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5943,
  "style_score": 0.41774043445300435,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "a8edf0e0-9326-4c65-8c4e-0e7d744d0b5c",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.4998,
  "style_score": 0.42661268712330636,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "ab821dd5-54ca-4e3c-98ff-90bac2dc07cb",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6401,
  "style_score": 0.35647804615814627,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "dd778737-657f-4ac5-bebc-0e3cce36f0f7",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5583,
  "style_score": 0.4919348976712607,
  "label": "We cannot confidently determine whether this text was written by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "e0b82378-f4e7-4a69-a81a-e2670d4dfe68",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "589c74aa-a19b-46ae-80fa-e7ae62bbb76c",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "99085f89-538b-40c1-8727-11179eb702a7",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "d1f96eda-b8f9-472d-ab06-bd5bf9cb1828",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "08306d28-ea80-4c95-bd64-e10c34068c9d",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.5,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "This text shows patterns commonly associated with AI-generated writing. However, this result does not prove that AI was used.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "58b2cdf2-3338-4f6b-954c-9d9443758920",
  "creator_id": null,
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.2395,
  "style_score": 0.5,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "1e9fbb99-8826-4963-b1fc-38c4ee7e2ab6",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0492,
  "style_score": 0.5,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 422,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 422,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 422,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 422,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
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
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "1c914ae3-9cf3-4c58-a534-7200b1b2aff0",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "96c88071-f933-4ba0-a4cc-1fe0f62b62ae",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "772dc55d-c6ed-42a1-9039-7660429d0075",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "7ec73169-9191-4d8b-8ec0-16fe4cf45e5b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "2ce16b7d-a32e-4d77-a10c-a08dbc8bc637",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "4c72f504-0e23-48d3-b820-325607f3e8b5",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this text was probably written by a person. However, this result cannot guarantee who wrote it.",
  "error": null,
  "verdict": ""
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
  "verdict": ""
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
  "verdict": ""
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
  "verdict": ""
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
  "verdict": ""
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
  "verdict": ""
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
  "verdict": ""
}
```
