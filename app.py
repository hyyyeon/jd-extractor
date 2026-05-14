from pathlib import Path

import streamlit as st

from jd_extractor.browser_selector import SelectionError, select_job_areas
from jd_extractor.storage import job_csv_bytes, job_txt_text, save_job_csv, save_job_txt


RESULTS_DIR = Path("results")


def init_state() -> None:
    if "job_data" not in st.session_state:
        st.session_state.job_data = None


def main() -> None:
    st.set_page_config(page_title="채용공고 JD 추출기", page_icon="📄", layout="wide")
    init_state()

    st.title("채용공고 JD 추출기")
    st.caption("채용공고 상세 페이지에서 제목과 본문 영역을 직접 클릭해 텍스트를 저장합니다.")

    with st.sidebar:
        st.header("설정")
        url = st.text_input("채용공고 상세 페이지 URL", placeholder="https://example.com/jobs/123")
        title_parent_depth = st.slider("제목을 더 큰 영역으로 잡기", 0, 3, 0)
        jd_parent_depth = st.slider("본문/JD을 더 큰 영역으로 잡기", 0, 6, 1)
        st.caption("본문이 너무 짧게 잡히면 ‘본문/JD를 더 큰 영역으로 잡기’ 값을 올린 뒤 다시 선택하세요.")

        start = st.button("영역 선택 시작", type="primary", use_container_width=True)
        reset = st.button("다시 선택", use_container_width=True)

    if reset:
        st.session_state.job_data = None
        st.rerun()

    if start:
        if not url.strip():
            st.error("먼저 채용공고 상세 페이지 URL을 입력하세요.")
        else:
            with st.spinner("Playwright 브라우저를 여는 중입니다. 열린 브라우저에서 안내에 따라 영역을 클릭하세요."):
                try:
                    st.session_state.job_data = select_job_areas(
                        url=url.strip(),
                        title_parent_depth=title_parent_depth,
                        jd_parent_depth=jd_parent_depth,
                    )
                except SelectionError as exc:
                    st.error(str(exc))
                except Exception as exc:  # Streamlit 화면에서 예상 밖 오류를 확인하기 쉽게 보여줍니다.
                    st.error(f"예상하지 못한 오류가 발생했습니다: {exc}")

    job_data = st.session_state.job_data
    if not job_data:
        st.info("왼쪽에 URL을 입력하고 '영역 선택 시작'을 누르세요.")
        return

    st.subheader("미리보기")
    col_title, col_meta = st.columns([2, 1])
    with col_title:
        st.text_input("추출된 제목", value=job_data["title"], disabled=True)
    with col_meta:
        st.text_input("출처 URL", value=job_data["source_url"], disabled=True)

    st.text_area("추출된 본문/JD", value=job_data["jd"], height=360)

    with st.expander("선택된 CSS selector 확인"):
        st.code(f"제목 selector: {job_data['title_selector']}", language="text")
        st.code(f"본문 selector: {job_data['jd_selector']}", language="text")

    st.subheader("저장")
    col_csv, col_txt = st.columns(2)
    with col_csv:
        if st.button("CSV로 저장", use_container_width=True):
            path = save_job_csv(job_data, RESULTS_DIR / "jobs.csv")
            st.success(f"저장 완료: {path}")
    with col_txt:
        if st.button("TXT로 저장", use_container_width=True):
            path = save_job_txt(job_data, RESULTS_DIR / "job.txt")
            st.success(f"저장 완료: {path}")

    col_download_csv, col_download_txt = st.columns(2)
    with col_download_csv:
        st.download_button(
            "CSV 다운로드",
            data=job_csv_bytes(job_data),
            file_name="jobs.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col_download_txt:
        st.download_button(
            "TXT 다운로드",
            data=job_txt_text(job_data),
            file_name="job.txt",
            mime="text/plain",
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
