# 채용공고 JD 추출기

비전공자도 채용공고 상세 페이지에서 제목과 본문 영역을 직접 클릭해 텍스트를 추출하고 `CSV` 또는 `TXT`로 저장할 수 있는 MVP입니다.

## 폴더 구조

```text
.
├── app.py
├── jd_extractor/
│   ├── __init__.py
│   ├── browser_selector.py
│   └── storage.py
├── results/
│   └── .gitkeep
├── requirements.txt
└── README.md
```

## 설치

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

환경에 따라 `python` 대신 `python3`를 사용해야 할 수 있습니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Windows PowerShell에서는 가상환경 활성화 명령만 다릅니다.

```powershell
.venv\Scripts\Activate.ps1
```

## 실행

```bash
streamlit run app.py
```

브라우저에 Streamlit 화면이 열리면 다음 순서로 사용합니다.

1. 왼쪽 입력창에 채용공고 상세 페이지 URL을 넣습니다.
2. `영역 선택 시작` 버튼을 누릅니다.
3. Playwright가 연 브라우저에서 안내에 따라 제목 영역을 클릭합니다.
4. 이어서 본문/JD 영역을 클릭합니다.
5. Streamlit 화면에서 추출 결과를 확인합니다.
6. `CSV로 저장`, `TXT로 저장` 또는 다운로드 버튼을 사용합니다.

저장 파일은 다음 위치에 생성됩니다.

```text
results/jobs.csv
results/job.txt
```

## 코드 흐름

`app.py`는 사용자가 보는 화면입니다. URL 입력, 부모 확장 단계 설정, 미리보기, 저장/다운로드 버튼을 담당합니다.

`jd_extractor/browser_selector.py`는 Playwright로 브라우저를 열고 페이지 안에 클릭 감지 스크립트를 넣습니다. 사용자가 영역을 클릭하면 해당 HTML 요소의 CSS selector와 `innerText`를 가져옵니다. 본문처럼 큰 영역이 필요한 경우에는 클릭한 요소의 부모 요소로 몇 단계 확장할지 설정할 수 있습니다.

`jd_extractor/storage.py`는 추출 결과를 `results/jobs.csv`와 `results/job.txt`로 저장합니다.

## 오류가 날 가능성이 높은 부분

### Playwright 브라우저가 설치되지 않은 경우

증상: `Executable doesn't exist` 같은 오류가 납니다.

해결:

```bash
playwright install chromium
```

### 페이지가 너무 오래 걸리거나 열리지 않는 경우

증상: 페이지 로딩 시간 초과 오류가 납니다.

해결: URL이 채용공고 상세 페이지가 맞는지 확인하고, 일반 브라우저에서 먼저 접속 가능한지 확인하세요.

### 클릭했는데 본문이 너무 짧게 추출되는 경우

원인: `p`, `span` 같은 작은 요소를 클릭했을 가능성이 큽니다.

해결: 왼쪽 설정의 `본문/JD 선택 후 부모 확장 단계`를 2~4 정도로 올린 뒤 `다시 선택`하세요.

### 로그인, 캡차, 접근 제한 페이지인 경우

이 MVP는 로그인, 캡차, 접근 제한 우회 기능을 제공하지 않습니다. 사용자가 직접 접근 가능한 공개 상세 페이지만 대상으로 합니다.

### CSS selector가 항상 재사용 가능하지는 않은 경우

동적으로 생성되는 사이트는 class 이름이나 DOM 구조가 매번 바뀔 수 있습니다. 이 MVP에서는 선택 당시의 selector를 기록해 확인용으로 남깁니다.
