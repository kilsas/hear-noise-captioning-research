# HEAR — Real-Time Speech Captioning Under Environmental Noise

**HEAR** is a browser-based real-time captioning system built to help Deaf and
Hard-of-Hearing (DHH) users follow spoken conversation. This repository
contains the noise-robustness research conducted on HEAR: a controlled study
of how environmental noise affects captioning accuracy and latency in English
and Korean, plus a lightweight post-processing filter developed from the
study's findings.

> **TL;DR:** I built HEAR, tested it under four levels of environmental noise
> across English and Korean (336 trials, 12 participants), found that word
> error rate and latency both increase with noise — and that Korean is
> disproportionately affected under high noise — then built and measured a
> lightweight post-processing filter that reduces error rate by up to 6.6%
> under high-noise conditions.

---

## Repository structure

```
.
├── README.md                  <- you are here
├── research/                  <- the papers
│   ├── HEAR_Noise_Captioning_Study_Report.docx      (main paper + Appendix A)
│   └── HEAR_Noise_Captioning_Study_Protocol.docx    (pre-registered protocol)
├── data/
│   ├── trial_log.csv          <- all 336 trials (ground truth, caption output, S/D/I, latency)
│   └── error_log.csv          <- 504 individually classified error instances
├── analysis/
│   ├── wer.py                 <- word-level edit-distance WER calculator
│   ├── crosscontamination_filter.py   <- the post-processing filter (Appendix A)
│   └── run_analysis.py        <- reproduces every number in Table 1 and Appendix A from the raw CSVs
└── docs/
    ├── methodology.md         <- study design summary
    └── architecture.md        <- system + experiment architecture
```

## Reproducing the results

```bash
cd analysis
python run_analysis.py
```

This reads `data/trial_log.csv` directly and recomputes Word Error Rate,
latency, and error-type counts for every language x noise-condition cell —
independently of the manually logged Substitution/Deletion/Insertion counts
in the CSV — using a standard word-level edit-distance alignment
(`wer.py`). It then applies the Appendix A post-processing filter
(`crosscontamination_filter.py`) and prints the before/after comparison.
Both outputs match the numbers reported in the paper.

## What this project actually found

| Question | Finding |
|---|---|
| Does noise increase caption error rate? | Yes, in both languages, monotonically (English: 0.022 → 0.555; Korean: 0.097 → 0.867 from clean to high noise). |
| Does noise increase latency? | Yes, in both languages, monotonically (≈670 ms clean → ≈1,400 ms high noise). |
| Is Korean more noise-sensitive than English? | Yes at every noise level, though the gap does not widen smoothly — it is dramatically larger only once noise reaches moderate-to-high levels. |
| What kind of errors dominate? | Substitution throughout, though deletions grow disproportionately fast in Korean under high noise — a more severe failure mode, since a dropped word gives no signal that anything was missed. |
| Can a simple post-processing rule help? | Modestly. A filter that removes caption words traceable to cross-sentence vocabulary contamination reduced WER by 3.2% overall and up to 6.6% under English high noise — a real but limited effect (see Appendix A for honest limitations). |

## Honest limitations (also documented in the paper)

- Noise conditions were presented in a **fixed order** (not randomized) for
  each participant, so the reported noise trends are confounded with
  time-on-task effects and cannot be attributed to noise alone with full
  confidence. This is the single biggest methodological weakness and the
  top priority for a follow-up study.
- The 42 trials per language x noise cell are **not independent** — they are
  7 trials nested within 6 participants. The effective sample size is closer
  to 6 than to 42.
- Error-type classification was done by a **single annotator**.
- The post-processing filter in Appendix A only works because the study used
  a small, **closed set of seven known sentences** per language; it does not
  directly generalize to open-vocabulary, real-world captioning.

See Section 8 (Limitations) of the main paper and Appendix A.4 for full detail.

## Status

- Pilot phase (n=2/language) completed, expanded to full study (n=6/language, 336 trials).
- Manuscript submitted to the IYRC Journal (under review).
- Post-processing filter (Appendix A) is an exploratory proof-of-concept; a
  follow-up study evaluating it as a standalone contribution is planned.

## Author

Sinyoung Kim, Daegu International School — kimlucy0901@gmail.com
