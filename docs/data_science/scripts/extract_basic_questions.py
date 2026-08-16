"""Render question-only pages from the Level 2 basic textbook.

The source alternates each question page with its explanation page:
set 1 starts at PDF page 613 and set 2 at PDF page 654 (1-based).
"""

from pathlib import Path
import glob
import os

import fitz


PDF_DIR = Path("pdf")
OUTPUT_DIR = Path("extracted_questions/images")


def find_source_pdf():
    candidates = [
        Path(path)
        for path in glob.glob(str(PDF_DIR / "*.pdf"))
        if 60_000_000 < os.path.getsize(path) < 100_000_000
    ]
    if len(candidates) != 1:
        raise RuntimeError("Could not uniquely identify the basic textbook PDF")
    return candidates[0]


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    document = fitz.open(find_source_pdf())

    # Zero-based pages: set 1 Q1=612, set 2 Q1=653; each answer follows its question.
    for set_number, first_page in ((1, 612), (2, 653)):
        for question_number in range(1, 21):
            page_index = first_page + (question_number - 1) * 2
            pixmap = document[page_index].get_pixmap(
                matrix=fitz.Matrix(1.5, 1.5), alpha=False
            )
            output = OUTPUT_DIR / f"set{set_number}_q{question_number:02d}.png"
            pixmap.save(str(output))

    print(f"Rendered 40 question pages to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
