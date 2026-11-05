# 두산밥캣 (Doosan Bobcat) PM 디렉토리

두산밥캣 축사 로더 자율화 프로젝트의 PM 컨텍스트를 모아 둔 디렉토리입니다. 사내 위키(Outline), Slack, Google Drive, Linear에 흩어진 내용을 로컬 문서로 정리해 유지하며, **1차프로젝트(수행 중인 PoC 계약)**와 **2차프로젝트(협상 중인 후속 계약)**로 나눠 관리합니다.

에이전트는 작업 전에 [`agents.md`](./agents.md)를 먼저 읽습니다.

## 🧭 디렉토리 안내

| 경로 | 내용 |
| :--- | :--- |
| [`agents.md`](./agents.md) | 에이전트 지침. 소스 규격, 1차와 2차 구분 규칙, 증분 수집 절차, 보안 등급 |
| [`sync_state.md`](./sync_state.md) | 소스별 마지막 동기화 기준점과 초기 수집에서 읽지 않은 범위 |
| [`stakeholder_contacts.md`](./stakeholder_contacts.md) | 두산밥캣, 마음AI, 현장, 협력사 관련자와 연락처 (두 프로젝트 공통) |
| [`1차프로젝트/project_status.md`](./1차프로젝트/project_status.md) | 1차 현황 종합. 계약 조항, 마일스톤과 대금, 영역별 현재 상태, 리스크 |
| [`1차프로젝트/document_index_snapshot.md`](./1차프로젝트/document_index_snapshot.md) | Drive와 Outline 문서 색인 |
| [`1차프로젝트/timeline/`](./1차프로젝트/timeline/) | 2026-02부터의 월별 연대기 (출처 링크 포함) |
| [`2차프로젝트/project_status.md`](./2차프로젝트/project_status.md) | 2차 협상 현황. 범위, 견적, 일정, 쟁점 |
| [`2차프로젝트/document_index_snapshot.md`](./2차프로젝트/document_index_snapshot.md) | 2차 관련 문서 색인 |
| [`2차프로젝트/timeline/`](./2차프로젝트/timeline/) | 2차 논의의 월별 연대기 |
| [`2차프로젝트/meetings/`](./2차프로젝트/meetings/) | 회의 전사본과 회의록 |

"2차 시연"(2026-11-12)은 1차프로젝트의 두 번째 시연이므로 1차 문서에 있습니다.

아래 두 문서는 1차에서 만든 데이터 툴체인을 다른 과제에 재사용하려고 2026-10-26에 정리한 참고 자료입니다.

---

## 📂 참고 문서: 데이터 툴체인과 재사용 계획

1. [**`bobcat_data_tools.md` (두산밥캣 자체 개발 데이터 툴 종합 분석 보고서)**](./bobcat_data_tools.md)
   * 밥캣 자율화/텔레옵 프로젝트에서 개발된 7대 핵심 데이터 인프라 상세 스펙:
     1. **WoRV Data Viewer**: 웹 기반 MCAP 브라우저 및 경량 시각화 툴 (`@mcap/core` 기반 클라이언트 사이드 파싱)
     2. **WoRV Labeling Tool**: 다채널 비디오 동기화, 서브태스크(Skill) 분할, 지시문(Instruction) 및 개입(Intervention) 라벨링 플랫폼
     3. **MCAP Trajectory & Anomaly Viewer**: 카메라-오도메트리 동기화 및 5대 이상치(`odom_missing`, `stuck`, `frozen`, `pose_jump`, `yaw_jump`) 자동 감지 로컬 뷰어
     4. **WoRV Eval Viewer**: 모델 롤아웃 추론 시각화 및 폐루프 평가 대시보드
     5. **Storage DB & Catalog Worker (`manage-storagedb`)**: Ceph 분산 스토리지 및 Slurm 배치 비디오 추출/프레임 누락 검증 워커
     6. **신호 기반 자동 라벨러**: 제어 명령 및 CAN 신호 분석을 통한 83%+ 동작 자동 분할 알고리즘
     7. **VLA 데이터셋 전처리 파이프라인 (`loaderdrive`)**: System 1 Refs Dataset (15/30Hz) 및 System 2 HuggingFace 변환기
   * 각 툴별 **웹 접속 주소, DB 접속 방식, GitHub 리포지토리 주소, 배포 환경** 수록.

2. [**`hanwha_ocean_reuse_strategy.md` (한화오션 계약·제안서 기반 데이터 툴 재사용 계획서)**](./hanwha_ocean_reuse_strategy.md)
   * **공식 계약 및 제안서 기준 요구사항**:
     * 총 **80시간, 1,600 에피소드** (무아크 50h, 단순용접 20h, U-Cell 모사 10h)
     * 수집 하드웨어: 한화로보틱스 HCR-5W + YAM Leader, Fronius TPS 500i, Basler 2D, WELDVIS HDR 비전, Keyence 레이저, Mech-Mind 3D
     * 계약 산출물 규격: **LeRobot v2.1 (O-A-S-P-E-M)** 오픈 포맷 및 한화오션 자체 재학습/파인튜닝 MLOps 환경 제공
   * **툴체인별 구체적 이식 계획**:
     * `WoRV Data Viewer`: Fronius 실시간 용접 전압/전류 파형 및 WELDVIS 영상 표출 웹 포털 및 납품용 SQLite 카탈로그 뷰어 활용.
     * `WoRV Labeling Tool`: `label.worvgrip.com/hanwhaocean` 분기 활성화 및 용접 6단계 서브태스크, 숙련 용접사 개입 라벨링.
     * `MCAP Trajectory Viewer`: 아크 소호, 토치 고착(모재 관통 방지), 로봇 특이점 감지 알고리즘 적용으로 현장 1차 불량 필터링.
     * `manage-storagedb`: 현장 NAS ↔ Ceph 동기화, `cam_gaps.json` 기반 동기화 5ms/프레임 누락 검증, MongoDB Atlas 메타데이터 인덱싱.
     * `신호 기반 자동 라벨러`: Fronius 아크/전류 디지털 신호를 이용한 95%+ 자동 세그멘테이션 (라벨링 공수 80% 절감).
     * `LeRobot v2.1 변환`: O-A-S-P-E-M 표준 Parquet 데이터셋 원클릭 빌더 구축.

---

## 🔗 핵심 툴 및 시스템 바로가기 요약

| 툴 명칭 | 서비스 접속 URL | GitHub 리포지토리 |
| :--- | :--- | :--- |
| **WoRV Data Viewer** | [https://worv-data-viewer.teleport.svc.internal.maum.ai/](https://worv-data-viewer.teleport.svc.internal.maum.ai/) | [MaumAI-Company/worv-data-viewer](https://github.com/MaumAI-Company/worv-data-viewer)<br/>배포: [infra.worv-data-viewer](https://github.com/MaumAI-Company/infra.worv-data-viewer) |
| **WoRV Labeling Tool** | [https://label.worvgrip.com/](https://label.worvgrip.com/) | [MaumAI-Company/labeling](https://github.com/MaumAI-Company/labeling) |
| **MCAP Trajectory Viewer** | 로컬 웹 뷰어 (`http://localhost:8080`) | [MaumAI-Company/lidar_localization (tools)](https://github.com/MaumAI-Company/lidar_localization/tree/tools/mcap-trajectory-viewer) |
| **WoRV Eval Viewer** | [https://eval.worvgrip.com/](https://eval.worvgrip.com/) | [MaumAI-Company/worv-evalviewer](https://github.com/MaumAI-Company/worv-evalviewer) |
| **Storage DB & Catalog** | MongoDB Atlas (`mongodb+srv://...worv.wtfib9v.mongodb.net/`) | [MaumAI-Company/manage-storagedb](https://github.com/MaumAI-Company/manage-storagedb) |
| **VLA Dataset ETL** | Slurm 분산 배치 클러스터 | [MaumAI-Company/loaderdrive](https://github.com/MaumAI-Company/loaderdrive) |
