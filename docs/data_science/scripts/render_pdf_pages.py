"""Render selected 1-based PDF pages for visual QA."""

import argparse
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "pdf" / "(PC다운로드용) [Lv2] Data Science 기본 교재.pdf"
OUTPUT = ROOT / "교재정리" / "_audit" / "rendered_pages"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pages", nargs="+", type=int)
    parser.add_argument("--scale", type=float, default=1.5)
    args = parser.parse_args()

    OUTPUT.mkdir(parents=True, exist_ok=True)
    document = fitz.open(str(PDF))
    for page_number in args.pages:
        page = document[page_number - 1]
        pixmap = page.get_pixmap(
            matrix=fitz.Matrix(args.scale, args.scale),
            colorspace=fitz.csRGB,
            alpha=False,
        )
        target = OUTPUT / f"page_{page_number:03d}.png"
        pixmap.save(str(target))
        print(target)


if __name__ == "__main__":
    main()
