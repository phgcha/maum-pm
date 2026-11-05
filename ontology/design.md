# 2. 다섯 도구 위의 설계

> 기준일: 2026-11-02 (KST). 상위 문서 [README.md](./README.md). 플랫폼 비교는 [platforms.md](./platforms.md)

---

## 2.1 원칙: 포인터 그래프

- 각 도구의 네이티브 객체를 기록 시스템으로 두고, 그 위에 얇은 식별자와 매핑 층만 얹는다.
- 콘텐츠를 복제하지 않는다. 복제하는 순간 두 번째 진실 원천이 생긴다.
- 다섯 도구 모두 공식 MCP 서버가 있어 에이전트가 포인터를 따라 실시간으로 내용을 읽는다. Google Drive만 아직 개발자 프리뷰다.
- 클래스마다 기록 시스템은 하나다. 나머지 도구에는 링크나 색인만 둔다.

---

## 2.2 v1 핵심 클래스 12개

| 클래스 | 기록 시스템 | 식별자 | 현재 v0 대응 |
| :--- | :--- | :--- | :--- |
| Customer 고객사 | Linear Customer 객체 또는 레지스트리 | 고객 코드 | 디렉터리명 |
| Project 과제 | Linear Project | `P-WORV777-24` | 디렉터리, Outline 컬렉션, Slack 채널 |
| Partner 파트너와 거래처 | 레지스트리, 사람용은 Notion 데이터베이스 | 도메인 | R&R 표, `external` 제목 접두사 |
| Contract 계약 | Google Drive | 파일 ID | 스냅샷 2.1 표 |
| Milestone 마일스톤 | Linear Milestone | 프로젝트 내 이름 | M1~M5 |
| Deliverable 산출물 | Drive 파일과 Linear 티켓 | `MAI-HO-00N Rev.X` | 산출물 폴더 |
| Issue 티켓 | Linear Issue | `WORV777-NN` | 그대로 |
| Decision 결정 | Linear 댓글 또는 문서가 기록, Slack 퍼머링크는 증거 | 티켓과 첨부 URL | 1줄 요약과 링크 규칙 |
| Risk 리스크 | Linear 티켓과 라벨 | 티켓 번호 | 상태 캐시 2절 |
| Document 문서 | Drive, Outline, Notion 각각 | 파일 ID, urlId, 페이지 UUID | 스냅샷 상태 어휘 |
| Meeting 회의 | Notion 회의록 DB는 3급, Outline은 1급 | 날짜와 상대 | 그대로 |
| Person 담당자 | 이메일 | 이메일 | R&R 표 |

- Channel, Hardware, Dataset, Specimen 같은 유형은 프로젝트별 확장 클래스로 두고 핵심 12개에 넣지 않는다.
- 결정의 기록 위치를 Slack에서 Linear로 옮긴다. Slack Connect 채널의 보존과 삭제 권한은 메시지를 보낸 조직에 있어서 파트너가 쓴 결정 메시지를 우리가 통제할 수 없다.
- Linear Customer 객체가 컨소시엄 역할, 즉 주관, 협력, 공급을 표현할 수 있는지는 미확인이다. 불가하면 Partner는 레지스트리에만 둔다.

---

## 2.3 식별자와 링크 규율

| 규칙 | 구현 |
| :--- | :--- |
| 사람은 이메일로 식별 | Slack, Notion, Linear 모두 이메일 조회를 지원 |
| 프로젝트는 Linear 코드로 식별 | 디렉터리명, Outline 컬렉션, Drive 공유 드라이브, Slack 채널 설명에 같은 코드 기재 |
| 문서는 도구 고유 ID로 식별 | 제목과 슬러그는 바뀌므로 Drive 파일 ID, Outline urlId, Notion 페이지 UUID만 신뢰 |
| 프로젝트 허브는 Linear Project Resources | API `entityExternalLinkCreate`로 Notion 허브, Outline 컬렉션, Drive 폴더, Slack 채널 링크를 프로젝트에 등록. 레지스트리의 1차 사본 |
| 결정 증거는 Linear 첨부 | 첨부 URL은 티켓당 멱등 키이고 `attachmentsForURL`로 역조회 가능. URL 정규화 규칙이 없으므로 쿼리스트링 포함 여부를 통일 |
| Drive 태깅 | 파일 속성에 프로젝트 코드, Drive 라벨에 보안 등급. 라벨은 Business Standard 등 상위 에디션 전용, 조직당 150개 |
| Document 필수 속성 | owner, status, verified_on 세 가지. Notion 페이지 검증 기능과 Linear의 Update Missing 표시가 신선도 알림을 대신 수행 |

---

## 2.4 정의와 레지스트리의 저장 위치

| 대상 | 위치 | 이유 |
| :--- | :--- | :--- |
| 온톨로지 정의 | git의 LinkML YAML 파일 하나 | JSON Schema, Pydantic 모델, 문서 사이트를 생성하고 폐기 메타데이터를 지원 |
| ID 레지스트리 | git YAML이 원본, Notion 데이터소스에 사람용 미러 | 변경 이력과 검토가 가능하고 에이전트가 바로 읽음 |
| 에이전트 지침 | CLAUDE.md와 `.claude/rules/` 경로 스코프 규칙 | 규칙 파일은 해당 고객 디렉터리를 다룰 때만 로드되어 컨텍스트 비용 절감 |
| 삼중 복제 파일 | AGENTS.md 하나와 import 한 줄 | 현재 CLAUDE.md, AGENTS.md, GEMINI.md가 바이트 단위로 동일한 사본 |

---

## 2.5 4단계 프로토콜 매핑

프로토콜은 유지하되 각 단계의 역할이 바뀐다.

| 단계 | 지금 | 적용 후 |
| :--- | :--- | :--- |
| Local Anchor | 손으로 쓴 상태 캐시 | 야간 작업이 생성하는 정식 섹션과 손으로 쓰는 델타를 분리 |
| Delta Query | Linear, Slack 필터 | 공식 MCP 실시간 조회. 보고용 에이전트는 Linear 읽기 전용 엔드포인트 사용 |
| Pointer Jump | 댓글 속 Slack 링크 추적 | Linear 첨부 역조회로 링크와 티켓을 양방향 탐색 |
| Compaction | 에이전트가 캐시에 반영 | 스냅샷과 지표는 야간 배치가 갱신, 에이전트는 델타만 기록 |

---

## 2.6 동기화 전략

| 방식 | 장점 | 단점 | 용도 |
| :--- | :--- | :--- | :--- |
| 온디맨드 에이전트 조회 | 비용 없음, 항상 최신 | 레이트 리밋에 묶임, 세션마다 반복 | 대화형 질의 |
| 야간 스케줄 풀 | Drive 변경 API 증분 조회가 저렴 | 하루 지연 | 문서 색인, 지표 계산 |
| 웹훅 | 실시간 | 상시 수신 서버 필요, 벤더별 재시도 정책 상이 | v1 이후 |
| 실체화 그래프 DB | 다중 홉 질의 | 두 번째 진실 원천, 운영 부담 | 교차 프로젝트 질문이 생기기 전까지 보류 |

웹훅 재시도 정책 참고. Linear는 3회 실패 후 비활성화, Notion은 24시간 동안 8회 재시도하며 본문을 싣지 않음, Outline은 실패하는 훅을 자동 비활성화, Drive 채널은 만료 후 재등록 필요.

---

## 2.7 로드맵

| 시기 | 산출물 |
| :--- | :--- |
| v0, 2주 | 12 클래스를 담은 `ontology.yaml`, 프로젝트별 5개 도구 ID를 담은 `registry.yaml`, Linear 템플릿과 단일 선택 라벨 그룹, Document 필수 속성 3개, 결정 기록 규칙 개정, 역량 질문 25개, rules 파일, 삼중 복제 파일 통합, 리포지토리 첫 커밋과 내부 DB 주소 제거 |
| 파일럿, 6~8주 | 한화오션 과제 1개에 적용, 야간 점검 작업, 사전 등록 지표 3~5개, 주간 보고 초안 자동 생성 |
| v1 판단, 분기 말 | 교차 프로젝트 질문이 있으면 Onyx 또는 그래프 검토, 없으면 경량 유지. 질문 봇 확대 |

- 라벨 그룹은 2026년 10월부터 다중 선택을 지정할 수 있으므로, 단일 선택이 필요한 그룹은 그룹 유형을 명시한다.
- 리포지토리는 git 초기화만 되어 있고 커밋이 없다. v0 첫 작업으로 커밋하고, `DusanBobcat/README.md`의 내부 DB 주소를 제거한다.
