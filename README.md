# Classcard_Auto_Matching_Game_Matcher
클래스카드 매칭 게임 전용 툴


# 🤖 Classcard Match Bot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Selenium-4.0+-43B02A?style=for-the-badge&logo=selenium&logoColor=white" alt="Selenium">
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License">
</p>

<p align="center">
  <b>클래스카드(Classcard) 매칭 게임용 지능형 자동화 스크립트</b><br>
  단어 세트 데이터를 자동으로 분석·수집하고, 실시간 상태 변화를 감지하여 매칭 게임을 완벽하게 플레이합니다.
</p>

---

## 📌 주요 기능 (Features)

* **🔒 안전한 자동 로그인** : 사용자가 터미널에 입력한 계정 정보로 클래스카드 플랫폼에 자동 접속합니다.
* **📊 지능형 데이터 추출** : 세트 페이지(`/set/`) 진입 시 단어, 뜻, 오디오 소스까지 완벽하게 파싱하여 로컬 `JSON` 파일로 자동 백업합니다.
* **🎧 오디오 모드 매칭 지원** : 일반 텍스트뿐만 아니라, 오디오 재생을 듣고 맞추는 게임 모드도 자동으로 식별하여 대응합니다.
* **🔄 실시간 상태 변경 감지 (Status Changed)** : 게임이 리셋되거나 새로운 판이 시작되는 순간(`wrapper-learn` 클래스 변화)을 실시간으로 감지하여 데이터를 자동으로 최신화합니다.
* **⚡ 실시간 대시보드 및 안정성** : 터미널 창에 현재 매칭 성공 횟수와 점수를 실시간 출력하며, `0.75초` 추적 딜레이를 통해 서버 차단을 방지합니다.

---

## 🛠️ 기술 스택 (Tech Stack)

| 대분류 | 기술 스택 | 비고 / 용도 |
| :--- | :--- | :--- |
| **Language** | `Python 3.8+` | 전체 프로그램 코어 로직 제어 |
| **Automation** | `Selenium Webdriver` | 브라우저 인스턴스 제어 및 DOM 크롤링 |
| **Data Storage** | `JSON` | 학습 데이터 구조화 및 영구 저장 |

---

## 🚀 실행 및 사용 방법 (Getting Started)

### 1. 필수 라이브러리 설치
터미널을 열고 아래 명령어를 실행하여 셀레니움을 설치하세요.
```bash
pip install selenium

2. 스크립트 실행 및 조작 가이드
⚠️ 중요: 본 매크로는 로그인까지만 자동으로 수행하며, 학습할 단어장 선택 및 게임 시작은 사용자의 수동 조작이 필요합니다.

스크립트를 실행한 뒤 터미널 창에 아이디와 비밀번호를 입력합니다.

크롬 브라우저가 자동으로 켜지면, 학습하고자 하는 단어 세트 메인 페이지로 직접 이동합니다. (URL에 /set/이 포함되면 자동으로 데이터 수집이 시작됩니다.)

수집 완료 메시지(Data Saved.)가 출력되면, 매칭 게임을 클릭해 시작합니다.

게임 내부에서 판이 바뀌거나 상태가 변경되면 봇이 알아서 Status Changed. 메시지를 띄우고 정답 데이터를 재동기화하며 매칭을 이어갑니다.

💡 주의 사항 (Notice)
🖥️ 안정적인 탐지 주기
본 봇은 앤티-디텍션 및 서버 부하 최소화를 위해 루프 하단에 sleep(0.75) 주기가 세팅되어 있습니다. 게임 화면의 로딩 속도나 PC 사양에 따라 유연하게 작동합니다.

🎨 터미널 인코딩 안내
터미널 가시성을 위해 ANSI 색상 코드(\033[...])를 사용합니다. 구형 Windows 기본 명령 프롬프트(CMD)에서는 인코딩 문제로 글자가 깨질 수 있으니, 가급적 VS Code 내장 터미널 또는 Windows Terminal 환경에서 실행하는 것을 강력히 권장합니다.
