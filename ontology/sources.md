# 근거와 검증 메모

> 기준일: 2026-11-02 (KST). 상위 문서 [README.md](./README.md). 조사일 2026-10-30~31 기준이며 요금제와 기능은 바뀔 수 있음

---

## 1. 근거 URL

| 주제 | 출처 |
| :--- | :--- |
| 온톨로지 정의 | https://tomgruber.org/writing/definition-of-ontology |
| 역량 질문 방법론 | https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html |
| 온톨로지 기반 LLM 정확도 벤치마크 | https://arxiv.org/abs/2311.07509 |
| 실패 원인, Thoughtworks 2026-06 | https://www.thoughtworks.com/insights/blog/data-strategy/why-ontologies-matter-fail-build-anyway |
| Anthropic 컨텍스트 엔지니어링 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents |
| Anthropic 에이전트 평가 가이드 | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents |
| Claude Code 메모리, 규칙, 강제 수단 | https://code.claude.com/docs/en/memory |
| Claude Code 스케줄 작업 | https://code.claude.com/docs/en/web-scheduled-tasks |
| claude-code-action 스케줄 예시 | https://github.com/anthropics/claude-code-action/blob/main/docs/solutions.md |
| Palantir 온톨로지 핵심 개념 | https://www.palantir.com/docs/foundry/ontology/core-concepts |
| Linear MCP 읽기 전용 엔드포인트 | https://linear.app/docs/mcp |
| Linear 첨부 멱등성과 역조회 | https://linear.app/developers/attachments |
| Linear 필터 | https://linear.app/developers/filtering |
| Linear 웹훅 | https://linear.app/developers/webhooks |
| Linear 프로젝트 업데이트와 Update Missing | https://linear.app/docs/initiative-and-project-updates |
| Notion AI Linear 커넥터 요건 | https://www.notion.com/connections/notion-ai-connector-for-linear |
| Notion 엔터프라이즈 검색 | https://www.notion.com/help/enterprise-search |
| Notion MCP 지원 도구 | https://developers.notion.com/docs/mcp-supported-tools |
| Notion 페이지 검증 | https://www.notion.com/help/wikis-and-verified-pages |
| Outline 내장 MCP | https://www.getoutline.com/changelog/mcp |
| Outline 릴리스 | https://github.com/outline/outline/releases |
| Slack MCP와 실시간 검색 API 정식 출시 | https://slack.com/blog/news/mcp-real-time-search-api-now-available |
| Slack 엔터프라이즈 검색 데이터 소스 | https://slack.com/help/articles/39044407124755-Set-up-and-manage-Slack-enterprise-search |
| Slack Connect 보존 정책 | https://slack.com/help/articles/115004152843 |
| Google Drive MCP 서버 | https://developers.google.com/workspace/guides/configure-mcp-servers |
| Google Drive 라벨 | https://knowledge.workspace.google.com/admin/security/get-started-as-a-classification-labels-admin |
| Onyx 커넥터 목록 | https://docs.onyx.app/admins/connectors |
| Glean 커넥터 목록 | https://docs.glean.com/connectors/ |
| Neo4j MCP for Aura | https://neo4j.com/?p=425123 |
| Kuzu 아카이브 | https://github.com/kuzudb/kuzu |
| Graphiti | https://github.com/getzep/graphiti |
| GraphRAG 대 RAG 체계적 평가 | https://arxiv.org/abs/2502.11371 |
| LinkML 개요 | https://linkml.io/linkml/intro/overview.html |
| LinkML 폐기 절차 | https://linkml.io/linkml/howtos/deprecating-elements.html |
| Letta 공유 메모리 저장소 | https://docs.letta.com/concepts/shared-memory |
| Gartner 2025-02-26 AI 준비 데이터 예측 | https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk |
| MIT NANDA GenAI Divide 2025-07 | https://mlq.ai/media/quarterly_decks/v0.1_State_of_AI_in_Business_2025_Report.pdf |
| Atlassian State of Teams 2025 | https://www.atlassian.com/blog/state-of-teams-2025 |
| GitBook 문서 품질 조사 2026-10 | https://www.gitbook.com/blog/documentation-quality-research-2026 |
| Microsoft Fabric IQ 온톨로지 | https://learn.microsoft.com/fabric/iq/ontology/overview |

---

## 2. 검증 메모

반박 검증에서 수정되거나 조건이 붙은 사실. 문서 본문은 이 메모를 반영한 상태다.

| 주장 | 검증 결과 |
| :--- | :--- |
| Notion AI는 Business 이상에 무제한 포함 | 2025-05 발표는 무제한이었으나, 신규 워크스페이스 2026-10-19, 기존 2026-11-02부터 멤버당 월 Standard 1,500과 Select 500 크레딧으로 과금. 엔터프라이즈 검색은 Business에서 베타 표기 |
| Outline 내장 MCP는 2026-02 도입 | 2026-02-18 변경 로그는 공지 시점. 기능 자체는 v1.6.0, 2026-03-15 릴리스부터이며 기존 워크스페이스는 기본으로 꺼짐. v1.12.0부터 OAuth Client ID Metadata Documents 지원. 2026-04부터 이동과 삭제도 가능 |
| Outline MCP에 읽기 전용 범위 있음 | 미문서화. 엔드포인트 범위 지정 API 키는 있으나 MCP가 이를 존중하는지 미검증 |
| Kuzu 아카이브와 포크 | 2025-10-10 아카이브. Ladybug는 활성, bighorn은 2026-10-23 아카이브. Graphiti는 Kuzu 백엔드 폐기 표시 |
| Onyx Outline 커넥터 | 공식 커넥터 존재. 권한 동기화 목록에 없어 Document Access 설정으로만 통제. 2026-10-28 문서 개편으로 설정 가이드 완성 |
| Glean 커넥터 | 106개, Outline 없음. 미지원 소스는 Indexing API |
| Slack 엔터프라이즈 검색 커넥터에 Notion 포함 | 공식 도움말 목록에 Notion과 Linear 없음. Notion은 마케팅 페이지 로고로만 등장 |
| Slack MCP와 Slack Connect | 실시간 검색 API 문서는 Slack Connect 채널 포함을 명시. MCP 문서는 언급 없음 |
| Slack MCP는 관리자 승인 필수 | 워크스페이스의 일반 앱 승인 절차를 따름. 내부 앱과 디렉터리 게시 앱만 사용 가능 |
| Linear `project` null 필터는 서드파티 근거뿐 | Linear 공식 GraphQL 스키마의 NullableProjectFilter가 지원 |
| Linear 라벨 그룹은 단일 선택 고정 | 2026-10 변경 로그부터 다중 선택 지정 가능. 단일 선택은 명시 설정 |
| Linear 웹훅 범위 | Issues, Comments, Labels, Projects, Project updates, Documents, Initiatives, Cycles, Customers, Users 등 지원. Teams 미포함 |
| claude-code-action은 schedule 미지원 | solutions.md에 `on: schedule` 예시가 있고 security.md가 `schedule`과 `workflow_dispatch`를 명시. custom-automations.md의 "coming soon" 문구가 오래된 것 |
| Claude Code 스케줄 작업 요금제 | Pro, Max, Ultra, Team, Enterprise. Ultra는 Max 20x의 새 이름. 연구 프리뷰, 시간당 1회 초과 불가 |
| Neo4j Aura Free 한도 | FAQ 기준 노드 20만, 관계 40만. MCP for Aura는 2026-07-21부터 Free, Professional, Business Critical에 무료 포함 |
| Drive 라벨 에디션 | Frontline, Business Standard와 Plus, Enterprise Standard와 Plus, Education Standard와 Plus, Essentials 계열. Business Starter 미포함. 조직당 150개 |
| Google Drive MCP | 개발자 프리뷰. Developer Preview Program 가입과 AI 에이전트용 OAuth 클라이언트 필요. 2026-10-29 문서 기준 |
| MIT NANDA 내부 구축 성공률 | 외부 파트너십 약 67%, 내부 구축 약 33%로 두 배 차이. 2025-07 예비 보고서, 인터뷰 52건과 설문 153건 기반 |
| Gartner 정확도 80%와 비용 60% 예측 | 2026-09 연구 노트가 아니라 2025-06-17과 2026-05-11 보도자료 출처. 보도자료는 "컨텍스트 레이어" 표현 사용 |
| Sequeda 벤치마크 | 수치 일치. 저자 전원 data.world 소속, 2023년 GPT-4, 199개 테이블 중 13개 사용. 고복잡도 셀 수치가 본문과 표에서 38.5%와 38.7%로 불일치 |
| Thoughtworks 두 분기, 1년 | 원문 확인. 데이터 없는 실무자 추정 |
| GitBook 83% | 원문 확인. 표시는 조사 대상이지 확인된 오류가 아님. 전체 질문의 3분의 1이 완전히 답변되지 못함 |
| GraphRAG 비용 | 색인 구축 135초 대비 5,560~7,702초. 답 없는 질문 점수 96.01 대비 19.27, Llama-3.1-8B 기준. 논문 본문과 표의 토큰 수치가 불일치하므로 토큰 배수는 인용하지 않음 |
| Letta가 메모리 블록을 폐기 | 공식 폐기는 아님. "더 이상 권장하지 않음"과 "향후 폐기 가능" 표현. 공유 메모리 저장소는 git 저장소 |
| Linear 첨부 URL | 티켓당 멱등 키. URL 정규화 규칙 미문서화 |
| Dashworks 통합 목록의 "Coming soon" | 템플릿 잔재로 실제 표시되지 않음. Outline 없음 |

---

## 3. 미검증 또는 인용 금지

| 항목 | 상태 |
| :--- | :--- |
| Atlan의 "15% 미만 파일럿 통과", "67% 전문성 부족", "1,000만~2,000만 달러 온톨로지 세금" | 출처가 무기명 벤더 글로 추적됨. 인용 금지 |
| HBR 앱 전환 1,200회, Panopto 2018 지식 손실 수치 | 유료 벽 또는 오래된 자료. 인용 금지 |
| Gartner 2025-06-25 "에이전트 AI 프로젝트 40% 취소" | 미검증 |
| Microsoft Viva Topics 종료일 | 미검증 |
| 한국 기업 지식 공유 회피 연구, 2018 McKinsey와 대한상의 조사, 2025 한국은행 조사 | 원문 미검증 |
| Glean 좌석당 가격과 최소 계약 | 경쟁사와 리셀러 수치만 존재 |
| Linear Customer 객체의 컨소시엄 역할 표현 가능 여부 | 미확인 |
| Graphiti group_id 네임스페이스의 보안 경계 사용 | 참조 MCP 서버에 인증이 없어 배포 수준 통제 필요 |
| Slack 워크플로 폼의 필드 매핑과 요금제 조건 | 서드파티 가이드로만 확인 |
