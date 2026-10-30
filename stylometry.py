"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())

def sentence_length_spread(text: str) -> float:
    """
    A hint on what you're reaching for: the standard deviation of sentence
    lengths, probably divided by the mean so a long text and a short one are
    comparable. `statistics.stdev` is imported for you.

    Watch the edge case: a one-sentence submission has no spread at all, and
    `stdev` raises on fewer than two values. Decide what that should return
    before the attack set decides for you.
    """
    # Measures how much sentence lengths vary relative to their average.
    # Higher values indicate more variation (treated as more human-like).
    # Returns 0.0 when there is only one sentence.

    sentence_list = sentences(text)
    lengths = [len(words(sentence)) for sentence in sentence_list]

    if len(lengths) < 2:
        return 0.0

    mean_length = statistics.mean(lengths)

    if mean_length == 0:
        return 0.0

    return statistics.stdev(lengths) / mean_length


# Calculates the ratio of unique words to total words.
# Higher values indicate more varied vocabulary.

def type_token_ratio(text: str) -> float:
    word_list = words(text)

    if not word_list:
        return 0.0

    return len(set(word_list)) / len(word_list)

# Measures selected punctuation marks relative to text length.
def punctuation_density(text: str) -> float:    
    punctuation_marks = ",;:—–-"

    if not text:
        return 0.0

    count = sum(1 for char in text if char in punctuation_marks)

    return count / len(text)


# ── Combining them ───────────────────────────────────────────────────────────
def style_signal(text: str) -> float:
    """
    Combines sentence length spread and vocabulary diversity into a 0–1
    AI-likelihood score. Both measures receive equal weight (50% each).
    Punctuation density is calculated separately but excluded from the score.
    Higher scores indicate more AI-like writing.
    """
  
    spread = sentence_length_spread(text)
    vocabulary = type_token_ratio(text)

    spread_score = 1 / (1 + spread)
    vocabulary_score = 1 - vocabulary

    return (spread_score + vocabulary_score) / 2


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    #print("\nAll zeros? These are stubs — Milestone 4 is where you build them.")
