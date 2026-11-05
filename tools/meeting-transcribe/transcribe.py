"""mlx-whisper 한국어 전사. 단어 타임스탬프 포함 결과를 JSON으로 저장."""
import json
from pathlib import Path

MODEL = "mlx-community/whisper-large-v3-mlx"
SILENCE_SKIP_SEC = 2.0  # 무음 구간에서 생성되는 환각 텍스트 건너뛰기


def transcribe(audio: Path, out: Path, prompt: str | None = None) -> None:
    import mlx_whisper

    result = mlx_whisper.transcribe(
        str(audio),
        path_or_hf_repo=MODEL,
        language="ko",
        word_timestamps=True,
        initial_prompt=prompt,
        # False면 첫 30초 창 이후 initial_prompt가 초기화되어 용어 프롬프트가 무력화됨.
        # 반복 환각은 무음 건너뛰기와 merge 단계 잡음 필터로 억제
        condition_on_previous_text=True,
        hallucination_silence_threshold=SILENCE_SKIP_SEC,
        verbose=False,
    )
    tmp = out.with_suffix(".tmp")
    tmp.write_text(json.dumps(result, ensure_ascii=False, indent=1))
    tmp.replace(out)
    print(f"[transcribe] segments={len(result['segments'])} -> {out}")
