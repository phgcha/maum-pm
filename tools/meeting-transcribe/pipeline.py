"""회의 녹음 → 화자 구분 전사 파이프라인.

단계: ffmpeg 변환 → mlx-whisper 전사 → pyannote 화자 구분 → 병합(transcript.raw.md/json).
GPU 경합을 피하려고 순차 실행하며, 출력 파일이 있는 단계는 건너뛴다.
화자 수나 프롬프트를 바꿨다면 --force stt diar로 재실행해야 반영된다.

사용 예:
  uv run --project tools/meeting-transcribe python tools/meeting-transcribe/pipeline.py \
      ~/stt/20261029-bobcat/source.m4a --speakers 8 \
      --prompt-file tools/meeting-transcribe/prompts/DusanBobcat.txt
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

from diarize import diarize
from merge import merge
from transcribe import transcribe

STEPS = ("audio", "stt", "diar")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", type=Path, help="녹음 파일(m4a, mp3, mp4, wav 등)")
    p.add_argument("--out", type=Path, help="작업 디렉토리 (기본: 입력 파일 디렉토리)")
    p.add_argument("--speakers", type=int, help="정확한 화자 수 (알면 지정 권장)")
    p.add_argument("--min-speakers", type=int)
    p.add_argument("--max-speakers", type=int)
    p.add_argument("--prompt-file", type=Path, help="전사 정확도용 용어 프롬프트 텍스트 파일")
    p.add_argument("--force", nargs="*", choices=STEPS, default=[], help="다시 실행할 단계")
    return p.parse_args()


def timed(label: str, fn, *args, **kwargs) -> None:
    t0 = time.monotonic()
    fn(*args, **kwargs)
    print(f"[{label}] {time.monotonic() - t0:.0f}s", flush=True)


def to_wav(src: Path, dst: Path) -> None:
    tmp = dst.with_suffix(".tmp.wav")  # 중단 시 잘린 WAV가 재사용되지 않도록 완료 후 교체
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-ac", "1", "-ar", "16000", str(tmp)],
                   check=True)
    tmp.replace(dst)


def steps_to_run(forced: list, outputs: dict) -> set:
    """출력이 없거나 강제 지정된 단계. audio를 다시 만들면 하위 단계도 다시 실행."""
    run = {s for s in STEPS if s in forced or not outputs[s].exists()}
    return run | {"stt", "diar"} if "audio" in run else run


def main() -> int:
    args = parse_args()
    if not args.input.is_file():
        print(f"input not found: {args.input}", file=sys.stderr)
        return 1
    out = (args.out or args.input.parent).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    outputs = {"audio": out / "audio.wav", "stt": out / "stt.json", "diar": out / "diar.json"}
    prompt = args.prompt_file.read_text().strip() if args.prompt_file else None
    run = steps_to_run(args.force, outputs)
    skipped = sorted(set(STEPS) - run)
    if skipped:
        print(f"[skip] existing outputs reused: {skipped} (use --force to rerun)")

    if "audio" in run:
        timed("audio", to_wav, args.input, outputs["audio"])
    if "stt" in run:
        timed("transcribe", transcribe, outputs["audio"], outputs["stt"], prompt)
    if "diar" in run:
        timed("diarize", diarize, outputs["audio"], outputs["diar"],
              args.speakers, args.min_speakers, args.max_speakers)
    # 교정본(transcript.md)을 덮어쓰지 않도록 원본 병합 결과는 .raw로 저장
    merge(outputs["stt"], outputs["diar"], out / "transcript.raw")
    return 0


if __name__ == "__main__":
    sys.exit(main())
