# 플랫폼 지형과 시나리오별 추천

> 기준일: 2026-11-02 (KST). 상위 문서 [README.md](./README.md). 검증을 통과한 사실만 기재. 검증 메모는 [sources.md](./sources.md)

---

## 1. 범주별 비교

| 범주 | 대표 제품 | 호스팅과 라이선스 | Linear, Notion, Outline, Drive, Slack 연동 | 적합 시나리오 |
| :--- | :--- | :--- | :--- | :--- |
| 스키마 언어 | LinkML | OSS, Apache-2.0 | 정의 전용 | 경량, 모든 시나리오의 기반 |
| 에이전트 컨텍스트 파일 | CLAUDE.md, AGENTS.md, rules | 파일 | 공식 MCP 5종으로 실시간 조회 | 경량, 현재 방식의 정식화 |
| 공식 MCP 서버 | Linear, Notion, Outline, Slack은 정식 제공, Drive는 개발자 프리뷰 | 벤더 호스팅, Outline은 셀프호스팅 도메인에 `/mcp` | 각 도구 | 경량과 중간 |
| 엔터프라이즈 검색, 오픈소스 | Onyx | 커뮤니티판 MIT, 셀프호스팅 | 5종 모두 네이티브. Outline은 권한 동기화 없음 | 중간. 1급 컬렉션 분리 필요 |
| 엔터프라이즈 검색, SaaS | Glean | 견적가 | Linear, Notion, Slack, Drive. Outline 없음 | 엔터프라이즈 |
| 이미 보유한 검색 | Notion AI 엔터프라이즈 검색 | Business 이상, 2026년 10~11월부터 크레딧 과금 | Linear, Slack, Drive 커넥터. Outline 못 읽음 | Business 요금제면 저비용 보완 |
| 이미 보유한 검색 | Slack 엔터프라이즈 검색 | Enterprise+ 전용 | Drive 등. Linear, Notion, Outline 없음 | 부적합 |
| 그래프 DB | Neo4j AuraDB | SaaS, Free 티어 20만 노드, 호스팅 MCP 무료 포함 | 직접 적재 | v1 이후. 데이터 위치 검토 선행 |
| 그래프 DB, 임베디드 | Ladybug | OSS, MIT | 직접 적재 | 로컬 포인터 그래프. Kuzu는 2025년 10월 아카이브, bighorn 포크도 2026년 10월 아카이브 |
| 시간 지식 그래프 | Graphiti, Zep | Apache-2.0 | 직접 적재 | 결정과 리스크의 시간 변화 추적이 필요할 때 |
| 문서 GraphRAG | Microsoft GraphRAG, LightRAG | OSS | 직접 적재 | 비권장. 색인 시간 수십 배, 답 없는 질문에 환각 |
| 엔터프라이즈 온톨로지 플랫폼 | Palantir Foundry, Microsoft Fabric IQ, Stardog | 협상가, Fabric IQ 온톨로지는 프리뷰 | Linear, Outline 네이티브 없음 | 설계 참고 모델로만 |

---

## 2. 공식 MCP 서버 현황

| 도구 | 상태 | 인증 | 비고 |
| :--- | :--- | :--- | :--- |
| Linear | 정식 제공 | OAuth 또는 API 키 | 읽기 전용 엔드포인트 `/mcp/readonly` 제공. 읽기 권한만 가진 API 키 사용 가능 |
| Notion | 정식 제공 | OAuth | 사용자가 접근 가능한 콘텐츠로 제한. 커넥터 검색과 다중 데이터소스 SQL은 Business 이상에 Notion AI 필요 |
| Outline | 정식 제공, v1.6.0 이상 | OAuth 기본, API 키 가능 | 워크스페이스 단위 켜고 끄기만 지원. 읽기 전용이나 컬렉션별 범위는 미문서화. 2026년 4월부터 이동과 삭제도 가능 |
| Slack | 2026-02-17 정식 출시 | 사용자 토큰 OAuth, 검색 범위별 동의 | 내부 앱과 디렉터리 게시 앱만 사용 가능. Slack Connect 콘텐츠 포함 여부는 실시간 검색 API 문서에만 명시, MCP 문서는 언급 없음 |
| Google Drive | 개발자 프리뷰 | AI 에이전트용 OAuth 클라이언트 | Developer Preview Program 가입 필요. 야간 작업은 Drive REST 변경 API 사용 |

---

## 3. 시나리오별 추천

| 시나리오 | 구성 | 판단 |
| :--- | :--- | :--- |
| 경량, 새 인프라 0 | LinkML 스키마, ID 레지스트리, 공식 MCP, rules 파일, Linear 템플릿 | **이 조직에 맞는 선택** |
| 중간 | Onyx 셀프호스팅으로 5종 통합 검색을 추가하거나, Neo4j Aura와 Graphiti로 시간 그래프 운영 | 교차 프로젝트 질문이 반복될 때 검토 |
| 엔터프라이즈 | Glean 또는 Palantir | 현재 규모와 Outline 미지원을 고려하면 후보 아님 |

---

## 4. 후보 선정 메모

- **Onyx**가 Linear, Notion, Outline, Drive, Slack 다섯 가지를 모두 네이티브 커넥터로 지원하는 유일한 검색 제품이다. Outline 커넥터는 권한 동기화가 없어 Document Access 설정으로만 통제하므로, 1급 컬렉션은 색인 대상에서 제외하거나 별도 인스턴스로 분리한다.
- **Glean**은 커넥터 106개 중 Outline이 없다. 미지원 소스는 Indexing API로 직접 커넥터를 만들어야 한다.
- **Notion AI 엔터프라이즈 검색**은 Linear 커넥터를 쓰려면 Business 이상 요금제의 워크스페이스 오너와 Linear 관리자 권한이 필요하다. 신규 워크스페이스는 2026-10-19, 기존 워크스페이스는 2026-11-02부터 멤버당 월 크레딧으로 과금한다.
- **Slack 엔터프라이즈 검색**은 Enterprise+ 전용이며 공식 데이터 소스 목록에 Linear와 Notion이 없다.
- **Neo4j AuraDB**는 2026-07-21부터 Free, Professional, Business Critical 티어에 호스팅 MCP가 무료로 포함된다. Free 티어는 노드 20만 개, 관계 40만 개 한도다. 1급 식별자나 파트너명을 해외 호스팅 무료 티어에 둘 수 있는지 데이터 위치 검토가 먼저다.
- **Kuzu**는 2025-10-10 아카이브되었고, 포크 중 bighorn도 2026-10-23 아카이브되었다. Ladybug만 활성 포크다. Graphiti도 Kuzu 백엔드를 폐기 표시했다.
- **문서 GraphRAG**는 2026년 벤치마크에서 다중 홉 추론과 문서 간 요약에서만 우세했고, 단일 사실 조회에서는 열세이거나 동률이었다. 색인 구축 시간은 일반 RAG 135초 대비 5,560~7,702초였고, 답이 없는 질문에 대한 점수가 크게 낮았다.
- **엔터프라이즈 온톨로지 플랫폼**은 MCP를 지원하지만 협상가이고 파이프라인 구축 부담이 크며, Linear와 Outline 네이티브 커넥터가 없다. Palantir의 객체, 링크, 액션 구조는 에이전트 권한 설계의 참고 모델로만 쓴다.
