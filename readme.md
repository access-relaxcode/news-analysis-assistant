# AI 기업 뉴스 분석 서비스

뉴스 또는 기업 발표 본문을 입력하면 AI가 핵심 사실, 긍정·부정 요인, 불확실성을 정리하는 Python 웹 서비스입니다. 분석 결과를 디스코드로 전송할 수 있습니다.

## 제작 목적

주가 알림 봇에서 만든 전송 기능을 재사용하고, 단일 AI 분석가를 서비스로 구현했습니다. 향후 다중 에이전트 시스템에서 뉴스 분석 역할로 확장하기 위한 프로젝트입니다.

## 주요 기능

- Streamlit 웹 화면에서 뉴스 본문 입력
- Gemini API를 이용한 구조화된 JSON 분석
- 긍정·부정 해석과 원문 근거 분리
- 공백과 줄바꿈을 제거한 뒤 인용의 원문 포함 여부 검사
- 세션 내 분석 결과 유지
- 분석 보고서의 디스코드 전송
- 현재 세션의 현재 결과에 대한 전송 성공 후 버튼 비활성화
- 원문, 결과, 모델, 분석 버전, UTC 생성 시각을 JSON 파일로 저장

## 동작 흐름

뉴스 입력 → AI 분석 → JSON 변환 → 근거 검사 → 화면 표시 및 기록 저장 → 사용자 선택에 따라 디스코드 전송

## 설치 및 실행

Windows PowerShell 기준입니다. Python을 설치한 뒤 프로젝트 폴더에서 실행합니다.

### 1. 실행 환경 준비

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. 인증 정보 설정

Google AI Studio에서 Gemini API 키를 준비하고, 디스코드에서 전송할 채널의 웹훅을 생성합니다.

아래 명령에서 각 값을 입력합니다. 입력 내용은 화면에 표시되지 않습니다.

```powershell
$geminiKeyInput = Read-Host "Gemini API 키 입력" -AsSecureString
$env:GEMINI_API_KEY = [System.Net.NetworkCredential]::new("", $geminiKeyInput).Password

$discordWebhookInput = Read-Host "디스코드 웹훅 URL 입력" -AsSecureString
$env:DISCORD_WEBHOOK_URL = [System.Net.NetworkCredential]::new("", $discordWebhookInput).Password
```

설정은 현재 터미널에서 유지됩니다. 새 터미널에서는 다시 설정해야 합니다. 키와 웹훅 URL은 공개하지 않습니다.

### 3. 웹 화면 실행

같은 터미널에서 실행합니다.

```powershell
.\.venv\Scripts\python.exe -m streamlit run .\app.py
```

브라우저에서 본문을 입력하고 ‘분석하기’를 누릅니다. 결과를 확인한 뒤 ‘디스코드로 보내기’를 누르면 전송됩니다. 서버 종료는 터미널에서 Ctrl+C를 누릅니다.

Gemini 호출에는 계정의 사용 한도와 요금 정책이 적용됩니다.

## 근거 검사 테스트

AI 호출 없이 정상 인용의 통과와 숫자를 변경한 인용의 차단을 확인합니다.

```powershell
.\.venv\Scripts\python.exe .\test_evidence.py
```

## 분석 품질 평가

가상 자료 3건을 수동 평가했습니다. 이익 규모 증가를 수익성 개선으로 해석한 문제를 발견하고, 프롬프트를 v1부터 v3까지 개선했습니다. v3에서 동일 사례와 다른 두 사례를 다시 확인했습니다.

평가 기준, 결과, 수정 과정은 `evaluation.md`에 기록했습니다. 이 평가는 실제 뉴스 전반의 정확도나 투자 수익성을 검증한 결과가 아닙니다.

## 현재 범위와 한계

- 사용자가 입력한 본문을 분석하며, 뉴스를 자동 수집하지 않습니다.
- 인용 검사는 원문 포함 여부를 확인합니다. 해석의 타당성이나 사실 목록 전체를 자동 검증하지는 않습니다.
- 브라우저 세션이 초기화되면 화면의 결과와 전송 상태도 초기화됩니다.
- 디스코드 메시지는 2,000자를 초과하면 전송하지 않습니다.
- 매수·매도 주문 기능은 없습니다.