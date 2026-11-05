# Maum AI PM Multi-Project Router & Agent Guidelines

- **Workspace Root**: `/Users/pcha/maumAI/jdb/maum-pm`
- **Repository**: `https://github.com/phgcha/maum-pm.git`
- **Target Audience**: AI Agents (`claude-acp`, `antigravity-acp` / `agy`, `codex-acp`)
- **Role**: Multi-Project PM Assistant Router

---

## 1. Project Directory & Context Routing

본 리포지토리는 고객사별 독립된 PM 디렉토리 구조를 가지고 있습니다. 사용자가 특정 프로젝트와 관련된 요청(상태 분석, 티켓 관리, 이슈 요약, 보고서 작성 등)을 전달하면, **작업 착수 전 해당 프로젝트의 컨텍스트 지침 문서를 가장 먼저 로드**해야 합니다.

### 1.1 Hanwha Ocean (한화오션)
- **Target Path**: `HanwhaOcean/`
- **Primary Directive**: `HanwhaOcean/agents.md` (또는 `HanwhaOcean/CLAUDE.md`)
- **Action Rule**:
  - 한화오션(`P-WORV777-24`, 곡블록 AI 용접) 관련 요청 수신 시, **작업 전 반드시 `HanwhaOcean/agents.md`를 먼저 읽고 그 지침에 따른다**.
  - `agents.md`에 명시된 4대 소스(Linear, Outline, Slack, Notion) 규격과 4단계 점진적 컨텍스트 수집 프로토콜(Local Anchor → Delta Query → Pointer Jump → Compaction)을 엄격히 준수한다.
  - 무차별 전수 스캔(Full Crawl)을 금지하며, 로컬 캐시(`HanwhaOcean/project_status.md`)를 1차 기준으로 삼는다.

### 1.2 Dusan Bobcat (두산밥캣)
- **Target Path**: `DusanBobcat/`
- **Primary References**: `DusanBobcat/README.md`, `DusanBobcat/bobcat_data_tools.md`, `DusanBobcat/hanwha_ocean_reuse_strategy.md`
- **Focus**: WoRV Data Viewer, WoRV Labeling Tool 등 7대 자체 개발 데이터 툴체인 사양 및 재사용 계획, 후속 프로젝트 회의록(`DusanBobcat/meetings/`).

### 1.3 Hanwha Aerospace (한화에어로스페이스)
- **Target Path**: `HanwhaAerospace/`
- **Primary Reference**: `HanwhaAerospace/project_status.md`

### 1.4 Ontology (사내 온톨로지)
- **Target Path**: `ontology/`
- **Primary Reference**: `ontology/README.md`

---

## 2. Global Execution Directives

1. **Local Anchor First**: 외부 API를 호출하기 전에 리포지토리 내 로컬 문서(`project_status.md`, 프로토콜 문서 등)를 먼저 읽어 기본 컨텍스트를 확보한다.
2. **Security & Boundary**: 사내 비공개 문서(Outline, 비공개 계약 등)의 내용을 파트너사 공개 채널(Slack 공용 채널, Notion 공유 페이지)에 유출하지 않는다.
3. **Source Attribution**: 모든 상태 보고 및 답변 시 근거가 된 출처(Linear 티켓 번호, Slack 스레드 링크, 문서명 등)를 명시한다.
4. **Human-in-the-Loop**: 상태 변경, 티켓 삭제, 외부 메시지 전송 등 되돌릴 수 없는 쓰기 작업은 반드시 사용자의 확인을 거친 후 실행한다.

---

## 3. Git History & Auto Commit/Push Rule

본 리포지토리는 개인용 PM 문서 히스토리 추적을 목적으로 Git으로 관리되며, 별도의 코드 리뷰나 PR 없이 변경 이력을 남기는 것이 핵심입니다.

1. **작업 완료 후 커밋 확인 요청**:
   - 에이전트가 리포지토리 내 문서나 파일을 생성·수정하는 작업을 완료하면, 응답 시 변경된 파일 목록을 요약하고 **사용자에게 커밋 및 푸시 진행 여부를 질문**한다.
2. **사용자 승인 시 자동 Commit & Push**:
   - 사용자가 허락(승인)하면 에이전트는 즉시 다음 과정을 자동으로 실행한다:
     - `git status` 및 `git diff`로 변경분 확인 (민감 설정 파일이나 불필요한 대용량 바이너리 제외 확인)
     - 변경된 항목을 스테이징(`git add`)하고, 작업 내용을 명확히 파악할 수 있는 메시지로 커밋(`git commit`)
     - 원격 저장소(`origin main`)로 즉시 푸시(`git push`)
