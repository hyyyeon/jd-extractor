from __future__ import annotations

import csv
from io import StringIO
from pathlib import Path


CSV_COLUMNS = ["title", "jd", "source_url", "title_selector", "jd_selector"]


def save_job_csv(job_data: dict[str, str], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(job_csv_bytes(job_data))
    return path


def save_job_txt(job_data: dict[str, str], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(job_txt_text(job_data), encoding="utf-8")
    return path


def job_csv_bytes(job_data: dict[str, str]) -> bytes:
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=CSV_COLUMNS)
    writer.writeheader()
    writer.writerow({column: job_data.get(column, "") for column in CSV_COLUMNS})
    return buffer.getvalue().encode("utf-8-sig")


def job_txt_text(job_data: dict[str, str]) -> str:
    return (
        f"제목: {job_data.get('title', '')}\n"
        f"출처: {job_data.get('source_url', '')}\n"
        f"제목 selector: {job_data.get('title_selector', '')}\n"
        f"본문 selector: {job_data.get('jd_selector', '')}\n\n"
        f"{job_data.get('jd', '')}\n"
    )
