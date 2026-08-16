"""Compare the textbook's page-order section labels with Markdown heading order."""

import json
import re
from collections import defaultdict
from pathlib import Path

from build_page_coverage import repair


ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "교재정리"
INVENTORY = NOTES / "_audit" / "page_inventory.jsonl"
OUTPUT = NOTES / "_audit" / "원문_순서_대조.md"


def clean(text):
    text = repair(repair(text)).strip()
    return re.sub(r"\s+", " ", text)


def source_label(record):
    lines = [clean(item) for item in record["ocr_lines"] if clean(item)]
    if not lines:
        return "(텍스트 없음)"
    for line in lines:
        if re.match(r"^\d{1,2}\s+\S", line) and "Data Science" not in line:
            return line
    return lines[0]


def main():
    records = {}
    for line in INVENTORY.open("r", encoding="utf-8"):
        item = json.loads(line)
        records[item["pdf_page"]] = item

    grouped = defaultdict(list)
    for page in sorted(records):
        grouped[records[page]["chapter"]].append(records[page])

    note_by_number = {}
    for path in NOTES.glob("[0-9][0-9]_*.md"):
        note_by_number[int(path.name[:2])] = path

    out = ["# 원문 순서 대조표", "", "> 각 페이지에서 판독한 원문 절 제목과 현재 Markdown의 2단계 제목을 순서대로 비교한다.", ""]
    for chapter in range(1, 24):
        chapter_records = grouped[chapter]
        title = chapter_records[0]["chapter_title"]
        out.extend(["## {:02d}. {}".format(chapter, title), "", "### 원문 페이지 순서", ""])
        previous = None
        for record in chapter_records:
            label = source_label(record)
            if label != previous:
                out.append("- PDF {}쪽: {}".format(record["pdf_page"], label))
                previous = label

        note = note_by_number[chapter]
        headings = []
        for line in note.read_text(encoding="utf-8").splitlines():
            if line.startswith("## ") and line != "## 목차":
                headings.append(line[3:])
        out.extend(["", "### 현재 Markdown 순서", ""])
        out.extend("- " + heading for heading in headings)
        out.append("")

    OUTPUT.write_text("\n".join(out), encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
