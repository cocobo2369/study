"""OCR and inventory textbook pages 3-611, resumably, one JSON object per page."""

import argparse
import json
from pathlib import Path

import easyocr
import fitz
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "pdf" / "(PC다운로드용) [Lv2] Data Science 기본 교재.pdf"
OUT = ROOT / "교재정리" / "_audit" / "page_inventory.jsonl"

CHAPTERS = [
    (1, 3, 27, "통계분석개요"), (2, 28, 66, "통계량"),
    (3, 67, 100, "자료의 표현"), (4, 101, 126, "확률"),
    (5, 127, 155, "확률의 계산"), (6, 156, 179, "이산확률분포"),
    (7, 180, 203, "연속확률분포"), (8, 204, 229, "추론통계"),
    (9, 230, 260, "데이터처리1"), (10, 261, 285, "데이터처리2"),
    (11, 286, 319, "상관분석"), (12, 320, 345, "머신러닝개요1"),
    (13, 346, 370, "머신러닝개요2"), (14, 371, 398, "선형회귀분석1"),
    (15, 399, 426, "선형회귀분석2"), (16, 427, 453, "이항로지스틱회귀분석"),
    (17, 454, 474, "k-NN"), (18, 475, 505, "의사결정나무"),
    (19, 506, 527, "나이브베이즈"), (20, 528, 547, "k-Means 군집분석"),
    (21, 548, 566, "특성공학"), (22, 567, 586, "앙상블모델링"),
    (23, 587, 611, "랜덤포레스트"),
]


def chapter_for(page_no):
    for number, start, end, title in CHAPTERS:
        if start <= page_no <= end:
            return number, title
    raise ValueError(page_no)


def load_done(path):
    if not path.exists():
        return set()
    done = set()
    with path.open("r", encoding="utf-8") as stream:
        for line in stream:
            try:
                done.add(json.loads(line)["pdf_page"])
            except (ValueError, KeyError):
                pass
    return done


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=3)
    parser.add_argument("--end", type=int, default=611)
    parser.add_argument("--scale", type=float, default=1.5)
    args = parser.parse_args()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    done = load_done(OUT)
    reader = easyocr.Reader(["ko", "en"], gpu=False, verbose=False)
    document = fitz.open(str(PDF))

    with OUT.open("a", encoding="utf-8", newline="\n") as stream:
        for pdf_page in range(args.start, args.end + 1):
            if pdf_page in done:
                continue
            page = document[pdf_page - 1]
            native = page.get_text("text", sort=True).strip()
            try:
                pix = page.get_pixmap(matrix=fitz.Matrix(args.scale, args.scale), colorspace=fitz.csRGB, alpha=False)
                image = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
                ocr = reader.readtext(image, detail=0, paragraph=False, batch_size=4)
            except RuntimeError as error:
                # Some vector-heavy pages exceed MuPDF's display-list limit.
                # Keep the native layer and continue so one page cannot stop the audit.
                ocr = ["[렌더링 제한: {}]".format(error), native] if native else ["[렌더링 제한: {}]".format(error)]
            chapter, title = chapter_for(pdf_page)
            record = {
                "pdf_page": pdf_page,
                "chapter": chapter,
                "chapter_title": title,
                "native_text": native,
                "ocr_lines": ocr,
            }
            serialized = json.dumps(record, ensure_ascii=False)
            serialized = serialized.encode("utf-8", "replace").decode("utf-8")
            stream.write(serialized + "\n")
            stream.flush()
            print("page {} chapter {} lines {}".format(pdf_page, chapter, len(ocr)), flush=True)


if __name__ == "__main__":
    main()
