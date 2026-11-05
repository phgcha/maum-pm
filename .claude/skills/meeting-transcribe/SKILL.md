---
name: meeting-transcribe
description: 회의 녹음(Google Drive 링크 또는 로컬 파일)을 로컬에서 STT와 화자 구분으로 전사하고, 프로젝트 맥락으로 교정한 뒤 회의록을 작성할 때 사용. 녹음 파일, 회의 녹취, 전사, 화자 구분, 회의록 작성 요청에 적용.
---

# 회의 녹음 전사, 교정, 회의록 작성

로컬 Apple Silicon에서 `mlx-whisper`(전사)와 `pyannote`(화자 구분)를 실행한다. 녹음은 외부 서비스로 전송하지 않는다.

## 0. 입력 확인

| 항목 | 필수 | 비고 |
|---|---|---|
| 녹음 위치 | 필수 | Drive URL/파일 ID 또는 로컬 경로 |
| 프로젝트 | 필수 | `DusanBobcat`, `HanwhaOcean`, `HanwhaAerospace` 등. 루트 `CLAUDE.md` 라우팅에 따라 맥락 문서 로드 |
| 참석자 수 | 권장 | 알면 `--speakers N`, 모르면 `--min-speakers`/`--max-speakers` |
| 회의 일자, 제목 | 권장 | 파일명에서 추정 가능하면 그대로 사용 |
| 참석자 명단 | 선택 | 화자 라벨 실명 치환에 사용. 사용자가 확인한 매핑만 적용 |

## 1. 녹음 확보

작업 디렉토리는 리포지토리 밖 `~/stt/<YYYYMMDD>-<slug>/`이다. 녹음과 중간 산출물을 리포지토리에 넣지 않는다.

- Drive 파일: `mcp__google-drive__get_drive_file_download_url`(`user_google_email`, `file_id`)로 받은 뒤 `~/.workspace-mcp/attachments/`의 파일을 작업 디렉토리의 `source.<ext>`로 이동. 사내 비공개 파일은 `gdown`이 실패하므로 MCP를 우선 사용
- 로컬 파일: 작업 디렉토리로 복사

## 2. 전사 파이프라인 실행

사전 조건(최초 1회):
- `hf auth login` 완료, [pyannote/speaker-diarization-community-1](https://huggingface.co/pyannote/speaker-diarization-community-1) 이용 약관 동의. 미동의 시 `GatedRepoError 403`
- `uv sync --project tools/meeting-transcribe`

실행(리포지토리 루트 기준, **백그라운드 실행과 `timeout` 7200000 필수**, 기본 30분 제한에 걸리면 진행분이 저장되지 않음):

```bash
uv run --project tools/meeting-transcribe python tools/meeting-transcribe/pipeline.py \
  ~/stt/<dir>/source.m4a --speakers <N> \
  --prompt-file tools/meeting-transcribe/prompts/<Project>.txt \
  > ~/stt/<dir>/pipeline.log 2>&1
```

- 단계는 순차 실행(GPU 경합 방지)하고 출력이 있는 단계는 건너뜀. **화자 수나 프롬프트를 바꾸면 `--force stt diar`로 재실행**해야 반영됨. `--force audio`는 하위 단계까지 재실행
- 소요 시간(M3, 16GB, 1시간 녹음 기준): 전사 약 25~35분, 화자 구분 약 12분
- 산출물: `audio.wav`, `stt.json`, `diar.json`, `transcript.raw.md`, `transcript.raw.json`(원본 병합 결과, 재실행 시 덮어씀)
- 프로젝트 용어 프롬프트가 없으면 `prompts/<Project>.txt`를 새로 만든다. 맥락 문서의 고유명사와 제품명 위주로 약 200 토큰 이내 유지

## 3. 프로젝트 맥락 교정

원본 전사는 원거리 녹음일수록 오인식, 화자 경계 오류가 많다. 다음 순서로 교정한다.

1. **맥락 수집**: 프로젝트 맥락 문서(`<Project>/README.md`, `project_status.md` 등)와 용어 프롬프트를 읽고, `transcript.raw.md` 전체를 훑어 `오인식 → 교정` 용어집 작성. 맥락, 용어집, 규칙을 작업 디렉토리의 `correction_brief.md`로 저장
2. **분할**: 30분 이상 녹음은 약 15분 단위로 나누어 서브에이전트에 병렬 위임. 각 에이전트는 `correction_brief.md`를 읽고 담당 시간대를 `corrected_partN.md`로 저장
3. **교정 규칙**
   - 타임스탬프와 화자 라벨 유지. 문장이 화자 경계에서 잘린 경우만 앞뒤 발화를 합침
   - 용어집과 문맥으로 확실한 오인식만 교정. 추정 교정은 `(?)` 표시
   - 의미를 복원할 수 없는 구간은 `[불명확]`으로 대체. 내용 창작 금지
   - 맞장구("네. 네.")와 의미 없는 짧은 발화는 생략 가능
   - 숫자(금액, 수량, 일정)는 원문을 보존하고 불확실하면 `(?)` 표시
4. **통합**: 분할 결과를 합쳐 교정본을 만들고(5단계 저장 위치), 용어집을 파일 끝에 첨부. 작업 디렉토리의 `transcript.raw.*`는 원본으로 보존

## 4. 회의록 작성

교정본을 근거로 작성하며, 원문이 불명확한 내용은 확정 사실로 쓰지 않는다.

```markdown
# <회의명>

| 항목 | 내용 |
|---|---|
| 일시 | YYYY-MM-DD |
| 참석 | N명 (화자 라벨 또는 확인된 실명) |
| 출처 | Drive 파일명, 교정 전사본 경로 |
| 전사 품질 | 녹음 상태와 불명확 구간 비율 요약 |

## 요약
## 논의 내용 (주제별, 근거 타임스탬프 포함)
## 결정 사항
## 후속 조치 (담당, 기한; 불명확하면 "미정")
## 확인 필요 사항 (전사 불명확으로 검증이 필요한 내용)
```

## 5. 저장과 공유

- 저장 위치: `<Project>/meetings/<YYYY-MM-DD>_<제목>/transcript.md`, `notes.md`
- 회의록은 사내 비공개 자료로 취급. Slack, Notion, Linear 등 외부 게시는 사용자 확인 후 실행
- 새로 확인된 용어는 `prompts/<Project>.txt`에 반영해 다음 회의 전사 정확도 향상
