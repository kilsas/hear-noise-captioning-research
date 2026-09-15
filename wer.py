"""
wer.py

Word Error Rate (WER) calculation via word-level edit distance.

WER = (Substitutions + Deletions + Insertions) / N_reference_tokens

Tokenization: whitespace-separated, with sentence-final punctuation stripped.
This applies the eojeol (whitespace-unit) rule to Korean as well as English,
per the study protocol (Section 4.5).
"""

def tokenize(text):
    """Whitespace tokenization with basic punctuation stripping."""
    return text.replace(",", "").replace(".", "").replace("?", "").split()


def wer_ops(ref_tokens, hyp_tokens):
    """
    Compute word-level edit distance between reference and hypothesis token
    lists, returning (substitutions, deletions, insertions, n_reference_tokens).

    Uses standard Levenshtein dynamic programming with unit costs, then
    backtracks through the DP table to classify each edit operation.
    """
    n, m = len(ref_tokens), len(hyp_tokens)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if ref_tokens[i - 1] == hyp_tokens[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    i, j = n, m
    substitutions = deletions = insertions = 0
    while i > 0 or j > 0:
        if (i > 0 and j > 0 and ref_tokens[i - 1] == hyp_tokens[j - 1]
                and dp[i][j] == dp[i - 1][j - 1]):
            i, j = i - 1, j - 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            substitutions += 1
            i, j = i - 1, j - 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            deletions += 1
            i -= 1
        else:
            insertions += 1
            j -= 1
    return substitutions, deletions, insertions, n


def wer(reference, hypothesis):
    """Convenience wrapper: WER between two raw strings."""
    ref_tokens = tokenize(reference)
    hyp_tokens = tokenize(hypothesis)
    s, d, ins, n = wer_ops(ref_tokens, hyp_tokens)
    return (s + d + ins) / n if n else 0.0


if __name__ == "__main__":
    ref = "The meeting begins at three."
    hyp = "menu meeting close at three."
    s, d, i, n = wer_ops(tokenize(ref), tokenize(hyp))
    print(f"ref={ref!r} hyp={hyp!r}")
    print(f"S={s} D={d} I={i} N={n}  WER={(s+d+i)/n:.3f}")
