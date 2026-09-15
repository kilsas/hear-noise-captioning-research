"""
crosscontamination_filter.py

A lightweight, rule-based post-processing filter for HEAR's real-time
captioning output (see paper Appendix A: "Post-Hoc Error Analysis and a
Lightweight Correction Filter").

Motivation
----------
Manual review of the error log showed that many insertion errors under
noise were not arbitrary: the spurious word HEAR inserted frequently
matched a word from a *different* known test sentence, rather than a
truly random word. Example:

    "The package arrived this morning."  -- ground truth
    "The soup arrived this morning."     -- captioned under noise

"soup" is not a random word; it belongs to a different sentence in the
same closed test set (the restaurant scenario). This suggests the
recognizer sometimes confuses the current utterance with another
sentence from the same small vocabulary it was recently exposed to.

Filter design
-------------
For each known sentence, build a "foreign vocabulary" set: all words
that appear in the *other* sentences of the same language but not in
this sentence itself. Remove any caption word that is in the foreign
vocabulary and not also part of the correct sentence's own vocabulary.

The filter only removes words -- it never inserts anything -- so it
can only reduce Insertion/Substitution-type errors, never fix true
Deletions.

Important limitation (see paper Appendix A.4): this specific technique
only works because the study used a small, closed set of seven known
sentences per language. It does not directly generalize to open-
vocabulary, real-world captioning. A generalizable version would need
a domain-specific language model or a confidence-based rejection rule
instead of a fixed sentence list.
"""

from wer import tokenize, wer_ops

SENTENCES = {
    "English": {
        "S01": "The meeting begins at three.",
        "S02": "Please close the door behind you.",
        "S03": "Turn left at the next light.",
        "S04": "The package arrived this morning.",
        "S05": "Today we are going to discuss the nervous system and how signals travel through the body.",
        "S06": "Could you pass the menu, I think I want the soup and a salad tonight.",
        "S07": "Wait, so are we meeting Friday or Saturday, and who is bringing the food?",
    },
    "Korean": {
        "S01": "회의는 세 시에 시작합니다.",
        "S02": "나가실 때 문을 닫아 주세요.",
        "S03": "다음 신호등에서 좌회전하세요.",
        "S04": "소포가 오늘 아침에 도착했습니다.",
        "S05": "오늘은 신경계와 신호가 몸속을 이동하는 방식에 대해 이야기해 볼게요.",
        "S06": "메뉴판 좀 건네줄래요? 오늘은 수프랑 샐러드를 먹고 싶어요.",
        "S07": "잠깐, 그럼 금요일에 만나는 거예요 토요일에 만나는 거예요? 그리고 음식은 누가 가져와요?",
    },
}


def _build_vocab(sentences):
    own = {lang: {sid: set(w.lower() for w in tokenize(txt)) for sid, txt in d.items()}
           for lang, d in sentences.items()}
    foreign = {}
    for lang in sentences:
        foreign[lang] = {}
        for sid in sentences[lang]:
            others = set()
            for sid2, vocab2 in own[lang].items():
                if sid2 != sid:
                    others |= vocab2
            foreign[lang][sid] = others - own[lang][sid]
    return own, foreign


OWN_VOCAB, FOREIGN_VOCAB = _build_vocab(SENTENCES)


def apply_filter(caption, sentence_id, language):
    """Remove words from `caption` that are recognizable cross-sentence
    contamination (see module docstring). Returns the filtered string."""
    tokens = tokenize(caption)
    fv = FOREIGN_VOCAB[language][sentence_id]
    ov = OWN_VOCAB[language][sentence_id]
    kept = [w for w in tokens if not (w.lower() in fv and w.lower() not in ov)]
    return " ".join(kept)


if __name__ == "__main__":
    examples = [
        ("English", "S04", "The soup arrived this morning"),
        ("English", "S01", "menu meeting close at three"),
        ("English", "S03", "Turn at soup next light"),
    ]
    for lang, sid, cap in examples:
        ref = SENTENCES[lang][sid]
        filtered = apply_filter(cap, sid, lang)
        wer_before = sum(wer_ops(tokenize(ref), tokenize(cap))[:3]) / wer_ops(tokenize(ref), tokenize(cap))[3]
        wer_after = sum(wer_ops(tokenize(ref), tokenize(filtered))[:3]) / wer_ops(tokenize(ref), tokenize(filtered))[3]
        print(f"[{sid}] {cap!r} -> {filtered!r}")
        print(f"        WER {wer_before:.3f} -> {wer_after:.3f}\n")
