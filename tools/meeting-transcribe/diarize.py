"""pyannote 화자 구분. 화자 구간 목록을 JSON으로 저장."""
import json
import wave
from pathlib import Path

MODEL = "pyannote/speaker-diarization-community-1"


def load_wav(path: Path) -> tuple:
    """16-bit 모노 WAV 로드. torchaudio(torchcodec)의 ffmpeg 동적 라이브러리 의존 회피."""
    import numpy as np
    import torch

    with wave.open(str(path), "rb") as f:
        if f.getsampwidth() != 2 or f.getnchannels() != 1:
            raise ValueError(f"16-bit mono WAV required: {path}")
        pcm = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16)
        return torch.from_numpy(pcm.astype(np.float32) / 32768.0).unsqueeze(0), f.getframerate()


def diarize(audio: Path, out: Path, num_speakers: int | None = None,
            min_speakers: int | None = None, max_speakers: int | None = None) -> None:
    import torch
    from pyannote.audio import Pipeline

    pipeline = Pipeline.from_pretrained(MODEL)
    if torch.backends.mps.is_available():
        pipeline.to(torch.device("mps"))
    waveform, sample_rate = load_wav(audio)
    output = pipeline(
        {"waveform": waveform, "sample_rate": sample_rate},
        num_speakers=num_speakers,
        min_speakers=min_speakers,
        max_speakers=max_speakers,
    )
    # 겹침 없는 구간이 단어 타임스탬프 정렬에 적합. 구버전 출력 형식이면 일반 구간으로 대체
    annotation = (getattr(output, "exclusive_speaker_diarization", None)
                  or getattr(output, "speaker_diarization", output))
    turns = [
        {"start": round(t.start, 3), "end": round(t.end, 3), "speaker": spk}
        for t, _, spk in annotation.itertracks(yield_label=True)
    ]
    tmp = out.with_suffix(".tmp")
    tmp.write_text(json.dumps(turns, ensure_ascii=False, indent=1))
    tmp.replace(out)
    print(f"[diarize] turns={len(turns)} speakers={len({t['speaker'] for t in turns})} -> {out}")
