# 채용공고 JD 추출기

채용공고 상세 페이지에서 제목과 본문(JD)을 직접 클릭해 텍스트로 저장하는 도구입니다.

코드를 몰라도 URL을 입력하고 브라우저에서 원하는 영역을 클릭하면 CSV 또는 TXT 파일로 저장할 수 있습니다.

---

# 주요 기능

- 채용공고 제목 추출
- 채용공고 본문(JD) 추출
- 사용자가 직접 원하는 영역 선택
- 추출 결과 미리보기
- CSV 저장
- TXT 저장
- 다시 선택 기능
- 본문 영역 확장 선택 기능

---

# 기술 스택

- Python
- Streamlit
- Playwright

---

# 설치 방법

## 1. Python 설치

Python 3.10 이상 권장

설치 확인:

```bash
python3 --version
```

---

## 2. 프로젝트 다운로드

```bash
git clone <repository_url>
cd jd-extractor
```

또는 ZIP 다운로드 후 압축 해제

---

## 3. 가상환경 생성

Linux / macOS:

```bash
python3 -m venv .venv
```

Windows:

```bash
python -m venv .venv
```

---

## 4. 가상환경 활성화

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

---

## 5. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

---

## 6. Playwright 브라우저 설치

```bash
playwright install
```

Chromium 브라우저가 설치됩니다.

---

# 실행 방법

가상환경 활성화 후 실행:

```bash
streamlit run app.py
```

또는:

```bash
python -m streamlit run app.py
```

실행 후 브라우저에서 아래 주소 접속:

```text
http://localhost:8501
```

---

# 사용 방법

## 1. 채용공고 URL 입력

왼쪽 입력창에 채용공고 상세 페이지 URL을 입력합니다.

예시:

```text
https://example.com/jobs/123
```

---

## 2. 영역 선택 시작

`영역 선택 시작` 버튼을 누르면 Playwright 브라우저가 열립니다.

---

## 3. 제목 영역 클릭

브라우저에서 채용공고 제목 부분을 클릭합니다.

예시:

```text
백엔드 개발자 채용
```

---

## 4. 본문/JD 영역 클릭

채용공고 본문 또는 JD 영역을 클릭합니다.

예시:

```text
담당업무
자격요건
우대사항
기술스택
```

---

## 5. 추출 결과 확인

Streamlit 화면에서 추출된 결과를 미리 확인할 수 있습니다.

---

## 6. CSV/TXT 저장

추출 결과를 CSV 또는 TXT 파일로 저장할 수 있습니다.

저장 위치:

```text
results/jobs.csv
results/job.txt
```

---

# 제목을 더 큰 영역으로 잡기

제목을 클릭했을 때, 클릭한 글자만 가져올지 제목을 감싸는 더 큰 영역까지 가져올지 정하는 설정입니다.

보통 제목은 한 줄이기 때문에 `0`을 추천합니다.

추천값:

```text
0
```

---

# 본문/JD를 더 큰 영역으로 잡기

본문을 클릭했을 때, 클릭한 문장만 가져올지 본문 전체를 감싸는 더 큰 영역까지 가져올지 정하는 설정입니다.

본문은 여러 문단과 목록으로 구성되어 있는 경우가 많기 때문에 보통 `1 ~ 3` 정도를 추천합니다.

추천값:

```text
1 ~ 3
```

---

## 이런 경우 사용하세요

### 본문이 너무 짧게 추출될 때

예시:

```text
담당업무 한 줄만 추출됨
```

→ `본문/JD를 더 큰 영역으로 잡기` 값을 올린 뒤 다시 선택하세요.

---

### 메뉴나 다른 내용까지 같이 추출될 때

예시:

```text
상단 메뉴, 회사 정보까지 같이 추출됨
```

→ `본문/JD를 더 큰 영역으로 잡기` 값을 낮춘 뒤 다시 선택하세요.

---

# 주요 파일 설명

## app.py

- Streamlit UI
- URL 입력
- 결과 미리보기
- 다운로드 기능

---

## browser_selector.py

- Playwright 브라우저 실행
- 클릭 감지
- selector 생성
- 텍스트 추출

---

## storage.py

- CSV 저장
- TXT 저장
