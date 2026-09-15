# Architecture

## System overview

HEAR is a browser-based real-time captioning tool with two main modules used
in this study: a speech-to-caption pipeline, and an experience-simulation
module that presents realistic conversational scenarios (classroom,
restaurant, group conversation) used as the noise-condition context.

```mermaid
flowchart LR
    A[Microphone input] --> B[HEAR ASR / captioning engine]
    B --> C[Live caption display]
    B -.-> D[Caption output logged for research]
```

## Research pipeline (this repository)

```mermaid
flowchart TD
    S[7 known sentences x 4 noise levels x 12 participants] --> T[336 trials recorded]
    T --> W["wer.py — word-level edit distance"]
    W --> TAB[Table 1: WER / latency / error-type by language x noise]
    TAB --> D1["Discovery: insertion errors often match words<br/>from OTHER known sentences (cross-contamination)"]
    D1 --> F["crosscontamination_filter.py<br/>(Appendix A post-processing filter)"]
    F --> CMP[Before / After WER comparison]
```

## Data flow for reproducing results

```
data/trial_log.csv  ──┐
                       ├──> analysis/run_analysis.py ──> Table 1 numbers + Appendix A before/after
data/error_log.csv  ──┘         (uses wer.py + crosscontamination_filter.py)
```

Every number in the paper's Table 1 and Appendix A is derived directly from
`data/trial_log.csv` by `run_analysis.py` — there is no manual step between
the raw data and the reported statistics, so anyone can re-run the analysis
and get the same numbers.
