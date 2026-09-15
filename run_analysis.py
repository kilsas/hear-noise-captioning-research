"""
run_analysis.py

Reproduces the main paper's Table 1 (WER, latency, error-type counts by
language x noise condition) and Appendix A's before/after post-processing
comparison, directly from data/trial_log.csv and data/error_log.csv.

Usage:
    python run_analysis.py
"""

import csv
from collections import defaultdict
from wer import tokenize, wer_ops
from crosscontamination_filter import apply_filter, SENTENCES

DATA_DIR = "../data"


def load_trials(path=f"{DATA_DIR}/trial_log.csv"):
    trials = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if not row["caption_output"].strip():
                continue  # unfilled template rows
            trials.append(row)
    return trials


def summarize(trials):
    langs = ["English", "Korean"]
    codes = ["C0", "C1", "C2", "C3"]
    agg = defaultdict(lambda: {"S": 0, "D": 0, "I": 0, "N": 0, "n_trials": 0,
                                "latency_sum": 0})

    for t in trials:
        lang, sid, code = t["language"], t["sentence_id"], t["noise_code"]
        ref = tokenize(SENTENCES[lang][sid])
        hyp = tokenize(t["caption_output"])
        s, d, i, n = wer_ops(ref, hyp)
        key = (lang, code)
        agg[key]["S"] += s
        agg[key]["D"] += d
        agg[key]["I"] += i
        agg[key]["N"] += n
        agg[key]["n_trials"] += 1
        agg[key]["latency_sum"] += int(t["latency_ms"])

    print(f"{'Lang':8} {'Noise':6} {'Trials':7} {'WER':>7} {'MeanLat(ms)':>12} {'Sub':>5} {'Del':>5} {'Ins':>5}")
    for lang in langs:
        for code in codes:
            a = agg[(lang, code)]
            wer_val = (a["S"] + a["D"] + a["I"]) / a["N"] if a["N"] else 0
            mean_lat = a["latency_sum"] / a["n_trials"] if a["n_trials"] else 0
            print(f"{lang:8} {code:6} {a['n_trials']:7} {wer_val:7.3f} {mean_lat:12.1f} "
                  f"{a['S']:5} {a['D']:5} {a['I']:5}")
    return agg


def before_after_filter(trials):
    print("\n=== Appendix A: cross-contamination filter, before vs. after ===")
    langs = ["English", "Korean"]
    codes = ["C0", "C1", "C2", "C3"]
    before = defaultdict(lambda: [0, 0])  # [error_sum, N]
    after = defaultdict(lambda: [0, 0])
    changed = 0

    for t in trials:
        lang, sid, code = t["language"], t["sentence_id"], t["noise_code"]
        ref = tokenize(SENTENCES[lang][sid])
        hyp = t["caption_output"]
        s, d, i, n = wer_ops(ref, tokenize(hyp))
        before[(lang, code)][0] += s + d + i
        before[(lang, code)][1] += n

        filtered = apply_filter(hyp, sid, lang)
        if filtered != " ".join(tokenize(hyp)):
            changed += 1
        s2, d2, i2, n2 = wer_ops(ref, tokenize(filtered))
        after[(lang, code)][0] += s2 + d2 + i2
        after[(lang, code)][1] += n2

    print(f"Trials modified: {changed} / {len(trials)}\n")
    print(f"{'Lang':8} {'Noise':6} {'WER before':>11} {'WER after':>10}")
    for lang in langs:
        for code in codes:
            eb, nb = before[(lang, code)]
            ea, na = after[(lang, code)]
            print(f"{lang:8} {code:6} {eb/nb:11.4f} {ea/na:10.4f}")


if __name__ == "__main__":
    trials = load_trials()
    print(f"Loaded {len(trials)} trials\n")
    summarize(trials)
    before_after_filter(trials)
