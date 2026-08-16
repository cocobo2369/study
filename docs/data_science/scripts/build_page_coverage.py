"""Normalize OCR inventory and build human-checkable per-page coverage files."""

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "교재정리" / "_audit"
SOURCE = AUDIT / "page_inventory.jsonl"


def repair(text):
    """Repair CP949 bytes that an old Korean OCR model exposed as Latin-1."""
    try:
        candidate = text.encode("latin-1").decode("cp949")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text
    original_hangul = sum("가" <= ch <= "힣" for ch in text)
    repaired_hangul = sum("가" <= ch <= "힣" for ch in candidate)
    return candidate if repaired_hangul > original_hangul else text


def main():
    latest = {}
    with SOURCE.open("r", encoding="utf-8") as stream:
        for line in stream:
            record = json.loads(line)
            record["ocr_lines"] = [repair(item) for item in record["ocr_lines"]]
            latest[record["pdf_page"]] = record

    grouped = defaultdict(list)
    for page in sorted(latest):
        grouped[latest[page]["chapter"]].append(latest[page])

    raw_dir = AUDIT / "chapters"
    raw_dir.mkdir(parents=True, exist_ok=True)
    for chapter, records in grouped.items():
        title = records[0]["chapter_title"]
        path = raw_dir / ("{:02d}_{}.md".format(chapter, title))
        lines = ["# {:02d}. {} OCR 대조본".format(chapter, title), ""]
        for record in records:
            lines.extend([
                "## PDF {}쪽".format(record["pdf_page"]), "",
                "  \n".join(record["ocr_lines"]), "",
            ])
        path.write_text("\n".join(lines), encoding="utf-8")

    coverage = [
        "# PDF 페이지 반영표", "",
        "> 1~23단원 범위는 PDF 3~611쪽이다. `OCR 완료`는 페이지별 원문 판독이 끝났음을 뜻하며, `노트 반영`은 해당 단원 Markdown의 전면 대조 완료 상태다.", "",
        "| PDF 쪽 | 단원 | 판독 상태 | 노트 반영 | 페이지 첫 문구 |", "|---:|---:|---|---|---|",
    ]
    fully_reflected = set(range(1, 24))
    for page in range(3, 612):
        record = latest.get(page)
        if record:
            first = next((x for x in record["ocr_lines"] if x.strip()), "(문구 없음)")
            first = first.replace("|", "\\|")[:80]
            status = "OCR 완료"
            reflected = "완료" if record["chapter"] in fully_reflected else "대조 중"
            coverage.append("| {} | {:02d} {} | {} | {} | {} |".format(
                page, record["chapter"], record["chapter_title"], status, reflected, first))
        else:
            coverage.append("| {} | — | 대기 | 대기 | — |".format(page))
    (ROOT / "교재정리" / "페이지_반영표.md").write_text("\n".join(coverage) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
