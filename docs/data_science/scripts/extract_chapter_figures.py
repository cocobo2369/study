"""Crop selected explanatory figures without copying whole textbook slides."""

from pathlib import Path
import glob
import os

import fitz


def locate_paths():
    source = next(
        Path(path)
        for path in glob.glob("pdf/*.pdf")
        if 60_000_000 < os.path.getsize(path) < 100_000_000
    )
    notes = next(
        path.parent
        for path in Path(".").glob("*/*.md")
        if path.name == "README.md"
        and len(list(path.parent.glob("[0-9][0-9]_*.md"))) == 23
    )
    return source, notes / "images"


def main():
    source, output_dir = locate_paths()
    output_dir.mkdir(exist_ok=True)
    document = fitz.open(source)

    # page number (1-based), clip rectangle in PDF points, output name
    figures = [
        (290, fitz.Rect(130, 450, 940, 690), "correlation_method_matrix.png"),
        (293, fitz.Rect(118, 470, 1040, 770), "bivariate_normal_distribution.png"),
        (301, fitz.Rect(130, 425, 830, 755), "correlation_patterns.png"),
        (308, fitz.Rect(130, 305, 690, 560), "correlation_outlier_effect.png"),
        (351, fitz.Rect(115, 305, 1085, 625), "cross_validation.png"),
        (432, fitz.Rect(120, 405, 760, 800), "sigmoid_curve.png"),
        (491, fitz.Rect(115, 305, 1010, 715), "decision_tree_prediction.png"),
        (574, fitz.Rect(115, 360, 660, 675), "bagging_process.png"),
    ]

    for page_number, clip, filename in figures:
        pixmap = document[page_number - 1].get_pixmap(
            matrix=fitz.Matrix(1.6, 1.6), clip=clip, alpha=False
        )
        pixmap.save(str(output_dir / filename))

    print(f"Extracted {len(figures)} figures to {output_dir}")


if __name__ == "__main__":
    main()
