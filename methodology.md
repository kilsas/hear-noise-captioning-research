# Methodology

Full detail is in `research/HEAR_Noise_Captioning_Study_Protocol.docx` (pre-registered)
and Sections 3–5 of the paper. Summary:

## Design
Within-subjects, repeated measures. Each participant completed all
combinations of 7 sentences x 4 noise conditions in their assigned language
(28 trials/participant).

## Participants
n = 6 per language (English: E01–E06, Korean: K01–K06), 12 total, 336 trials.
Recruited voluntarily; minimal demographic data only (age group, self-reported
hearing status); no names or medical records collected.

## Materials
7 sentence pairs per language, drawn from HEAR's own screening and
experience-simulation modules (not researcher-authored filler text), so the
evaluation reflects real product content.

## Noise conditions
| Code | Condition | Playback level | Korean cohort noise source |
|---|---|---|---|
| C0 | Clean | 0 dB added | None |
| C1 | Low | ≈45 dB | Classroom background + indistinct voices |
| C2 | Moderate | ≈60 dB | Restaurant (dishes, nearby conversation) |
| C3 | High | ≈70 dB | Overlapping group conversation |

Recording device: laptop internal microphone, ≈50 cm from speaker, held
constant across all trials.

## Metrics
- **Word Error Rate (WER)** = (Substitutions + Deletions + Insertions) / N
  reference tokens. Tokenization is whitespace-based (eojeol rule) for both
  English and Korean.
- **Latency** = time from end of spoken sentence to final displayed caption (ms).
- Each individual discrepancy was also classified by error type
  (substitution / deletion / insertion) and logged separately
  (`data/error_log.csv`), independent of the aggregate WER.

## Known methodological limitations
See the paper's Section 8 and this repo's README for the full list —
most importantly, **noise conditions were presented in a fixed order rather
than randomized**, which confounds noise level with time-on-task.
