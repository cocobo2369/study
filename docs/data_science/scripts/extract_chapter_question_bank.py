"""Extract the five end-of-chapter questions for chapters 1-23.

The textbook pages are raster slides.  To avoid confusing a numeric option with
an option label, the four orange diamond labels are located first and every
option is OCRed from its own horizontal row.  The filled orange diamond on the
following explanation page determines the answer number.
"""

import argparse
import json
import re
from pathlib import Path

import easyocr
import cv2
import fitz
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "pdf" / "(PC다운로드용) [Lv2] Data Science 기본 교재.pdf"
OUTPUT = ROOT / "교재정리" / "_audit" / "chapter_question_bank_ocr.json"

# Inclusive, 1-based PDF page ranges.  Odd pages in each range contain a
# question; the immediately following page contains the marked answer.
QUESTION_RANGES = {
    1: (18, 27), 2: (57, 66), 3: (91, 100), 4: (117, 126),
    5: (146, 155), 6: (170, 179), 7: (194, 203), 8: (220, 229),
    9: (251, 260), 10: (276, 285), 11: (310, 319), 12: (336, 345),
    13: (361, 370), 14: (389, 398), 15: (417, 426), 16: (444, 453),
    17: (465, 474), 18: (496, 505), 19: (518, 527), 20: (538, 547),
    21: (557, 566), 22: (577, 586), 23: (602, 611),
}


def render(page, scale):
    pixmap = page.get_pixmap(
        matrix=fitz.Matrix(scale, scale),
        colorspace=fitz.csRGB,
        alpha=False,
    )
    return np.frombuffer(pixmap.samples, dtype=np.uint8).reshape(
        pixmap.height, pixmap.width, 3
    )


def orange_mask(image):
    red, green, blue = image[:, :, 0], image[:, :, 1], image[:, :, 2]
    return (red > 230) & (green > 75) & (green < 195) & (blue < 125)


def diamond_groups(image):
    """Return option diamonds as (left, top, right, bottom, orange count)."""
    height, width = image.shape[:2]
    mask = orange_mask(image).astype(np.uint8)
    component_count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    diamonds = []
    for label in range(1, component_count):
        left, top, box_width, box_height, area = [int(v) for v in stats[label]]
        if not (0.018 * width < box_width < 0.060 * width):
            continue
        if not (0.035 * height < box_height < 0.105 * height):
            continue
        if not (0.72 < box_width / float(box_height) < 1.32):
            continue
        if not (0.16 * height < top < 0.76 * height):
            continue
        # Filled diamonds and outlined diamonds have the same bounding box but
        # sharply different orange areas.  Keep both.
        diamonds.append((left, top, left + box_width, top + box_height, area))

    if not (2 <= len(diamonds) <= 4):
        raise RuntimeError("Expected two to four option diamonds, found {}".format(diamonds))

    x_centers = [(item[0] + item[2]) / 2 for item in diamonds]
    if len(diamonds) == 4 and max(x_centers) - min(x_centers) > 0.20 * width:
        # Two-column layout numbers options down the left column, then down the
        # right column (1,2 / 3,4).
        diamonds.sort(key=lambda item: ((item[0] + item[2]) / 2, (item[1] + item[3]) / 2))
    else:
        diamonds.sort(key=lambda item: (item[1] + item[3]) / 2)
    return diamonds


def clean_ocr(lines):
    text = " ".join(str(line).strip() for line in lines if str(line).strip())
    text = re.sub(r"\s+", " ", text).strip()
    return text


def read_crop(reader, image, left, top, right, bottom):
    height, width = image.shape[:2]
    crop = image[
        max(0, int(top * height)):min(height, int(bottom * height)),
        max(0, int(left * width)):min(width, int(right * width)),
    ]
    return clean_ocr(reader.readtext(crop, detail=0, paragraph=False, batch_size=4))


def extract_question(reader, question_image, answer_image):
    question_groups = diamond_groups(question_image)
    answer_groups = diamond_groups(answer_image)
    height, width = question_image.shape[:2]
    x_centers = [(left + right) / 2 for left, _, right, _, _ in question_groups]
    y_centers = [(top + bottom) / 2 for _, top, _, bottom, _ in question_groups]
    grid_layout = (
        len(question_groups) == 4
        and max(x_centers) - min(x_centers) > 0.20 * width
    )

    stem_bottom = (min(item[1] for item in question_groups) / height) - 0.025
    stem = read_crop(reader, question_image, 0.07, 0.00, 0.98, stem_bottom)
    stem = re.sub(r"^\d+\s*문제\s*풀이\s*", "", stem).strip()
    stem = re.sub(r"^Q\s*\d+[.\s]*", "", stem).strip()

    options = []
    for index, (left_px, top_px, right_px, bottom_px, _) in enumerate(question_groups):
        center_y = (top_px + bottom_px) / 2
        if grid_layout:
            same_column = [
                item for item in question_groups
                if abs(((item[0] + item[2]) / 2) - x_centers[index]) < 0.10 * width
            ]
            same_column.sort(key=lambda item: (item[1] + item[3]) / 2)
            position = same_column.index(question_groups[index])
            if position == 0:
                crop_top = center_y / height - 0.045
                next_center = (same_column[1][1] + same_column[1][3]) / 2
                crop_bottom = ((center_y + next_center) / 2) / height
            else:
                previous_center = (same_column[position - 1][1] + same_column[position - 1][3]) / 2
                crop_top = ((previous_center + center_y) / 2) / height
                crop_bottom = center_y / height + 0.050
            column_split = (min(x_centers) + max(x_centers)) / 2
            is_left_column = x_centers[index] < column_split
            crop_right = (
                min(
                    item[0] for item in question_groups
                    if (item[0] + item[2]) / 2 > column_split
                ) / width - 0.02
                if is_left_column else 0.98
            )
        else:
            if index == 0:
                crop_top = center_y / height - 0.045
            else:
                crop_top = ((y_centers[index - 1] + center_y) / 2) / height
            if index == len(y_centers) - 1:
                crop_bottom = center_y / height + 0.050
            else:
                crop_bottom = ((center_y + y_centers[index + 1]) / 2) / height
            crop_right = 0.98

        crop_left = (right_px / width) + 0.005
        options.append(
            read_crop(reader, question_image, crop_left, crop_top, crop_right, crop_bottom)
        )

    answer_counts = [group[4] for group in answer_groups]
    answer = int(np.argmax(answer_counts)) + 1
    explanation = read_crop(reader, answer_image, 0.07, 0.715, 0.98, 0.985)
    explanation = re.sub(r"^해설\s*", "", explanation).strip()
    return {
        "stem": stem,
        "options": options,
        "answer": answer,
        "answer_orange_counts": answer_counts,
        "source_explanation": explanation,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-chapter", type=int, default=1)
    parser.add_argument("--end-chapter", type=int, default=23)
    parser.add_argument("--scale", type=float, default=1.5)
    args = parser.parse_args()

    reader = easyocr.Reader(["ko", "en"], gpu=False, verbose=False)
    document = fitz.open(str(PDF))
    if OUTPUT.exists():
        extracted = json.loads(OUTPUT.read_text(encoding="utf-8"))
    else:
        extracted = []
    records = {
        (record["chapter"], record["question"]): record for record in extracted
    }

    for chapter in range(args.start_chapter, args.end_chapter + 1):
        first_page, last_page = QUESTION_RANGES[chapter]
        for question_number, question_page in enumerate(
            range(first_page, last_page + 1, 2), start=1
        ):
            key = (chapter, question_number)
            if key in records:
                print(
                    "chapter {:02d} question {} already extracted".format(
                        chapter, question_number
                    ),
                    flush=True,
                )
                continue
            answer_page = question_page + 1
            question_image = render(document[question_page - 1], args.scale)
            answer_image = render(document[answer_page - 1], args.scale)
            record = extract_question(reader, question_image, answer_image)
            record.update({
                "chapter": chapter,
                "question": question_number,
                "question_pdf_page": question_page,
                "answer_pdf_page": answer_page,
            })
            records[key] = record
            print(
                "chapter {:02d} question {} answer {}".format(
                    chapter, question_number, record["answer"]
                ),
                flush=True,
            )
            OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            OUTPUT.write_text(
                json.dumps(
                    [records[item] for item in sorted(records)],
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

    print("Wrote {} questions to {}".format(len(records), OUTPUT))


if __name__ == "__main__":
    main()
