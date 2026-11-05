"""STT 단어와 화자 구간을 병합해 화자별 발화 Markdown, JSON 생성.

- 단어마다 시간이 가장 많이 겹치는 화자 할당, 겹침이 없으면 가장 가까운 구간의 화자 사용
- 무음 환각 토큰(`.A`, `a`, `1.`, `...` 등)과 과도한 반복 제거
- 같은 화자의 연속 단어를 하나의 발화로 묶음
"""
import bisect
import json
import re
from pathlib import Path

MAX_GAP_SEC = 1.5  # 같은 화자라도 이 간격 이상 끊기면 새 발화
MAX_REPEAT_HANGUL = 2  # 한글 토큰 연속 반복 허용 횟수("네. 네.")
MAX_REPEAT_OTHER = 1  # 비한글 토큰 연속 반복 허용 횟수("1. 1. 1." 환각 억제)
LOW_PROB = 0.1  # 한글이 없는 토큰의 최소 신뢰도
MIN_WORD_SEC = 0.02  # 길이 0인 단어의 화자 매칭용 최소 길이
HANGUL = re.compile(r"[가-힣]")
DIGIT = re.compile(r"\d")
MEANINGFUL_LATIN = re.compile(r"[A-Za-z]{2,}")


def is_noise(word: dict) -> bool:
    text = word["word"].strip()
    if not text:
        return True
    if HANGUL.search(text):
        return False
    if word.get("probability", 1.0) < LOW_PROB:
        return True
    return not (DIGIT.search(text) or MEANINGFUL_LATIN.search(text))


def clean_words(words: list) -> list:
    kept, last, run = [], None, 0
    for w in words:
        if is_noise(w):
            continue
        key = w["word"].strip()
        run = run + 1 if key == last else 1
        last = key
        limit = MAX_REPEAT_HANGUL if HANGUL.search(key) else MAX_REPEAT_OTHER
        if run <= limit:
            kept.append(w)
    return kept


def iter_words(stt: dict):
    for seg in stt["segments"]:
        yield from seg.get("words") or [{"start": seg["start"], "end": seg["end"], "word": seg["text"]}]


def assign_speaker(start: float, end: float, turns: list, starts: list) -> str:
    end = max(end, start + MIN_WORD_SEC)
    idx = bisect.bisect_right(starts, end)
    best, best_overlap = None, 0.0
    for t in turns[:idx]:  # 긴 구간이 오래전에 시작했을 수 있어 창 제한 없이 검사
        overlap = min(end, t["end"]) - max(start, t["start"])
        if overlap > best_overlap:
            best, best_overlap = t["speaker"], overlap
    if best:
        return best
    mid = (start + end) / 2
    return min(turns, key=lambda t: min(abs(mid - t["start"]), abs(mid - t["end"])))["speaker"]


def build_utterances(words: list, turns: list) -> list:
    turns = sorted(turns, key=lambda t: t["start"])
    starts = [t["start"] for t in turns]
    utterances = []
    for w in words:
        spk = assign_speaker(w["start"], w["end"], turns, starts)
        last = utterances[-1] if utterances else None
        if last and last["speaker"] == spk and w["start"] - last["end"] < MAX_GAP_SEC:
            utterances[-1] = {**last, "end": w["end"], "text": last["text"] + w["word"]}
        else:
            utterances.append({"start": w["start"], "end": w["end"], "speaker": spk, "text": w["word"]})
    return [{**u, "text": u["text"].strip()} for u in utterances]


def fmt(sec: float) -> str:
    s = int(sec)
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def merge(stt_path: Path, diar_path: Path, out_stem: Path) -> None:
    stt = json.loads(stt_path.read_text())
    turns = json.loads(diar_path.read_text())
    words = list(iter_words(stt))
    cleaned = clean_words(words)
    utterances = build_utterances(cleaned, turns)
    Path(f"{out_stem}.json").write_text(json.dumps(utterances, ensure_ascii=False, indent=1))
    lines = [f"**[{fmt(u['start'])}] {u['speaker']}**: {u['text']}\n" for u in utterances]
    Path(f"{out_stem}.md").write_text("\n".join(lines))
    print(f"[merge] words={len(words)} dropped={len(words) - len(cleaned)} "
          f"utterances={len(utterances)} -> {out_stem}.md")
