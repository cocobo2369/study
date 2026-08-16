"""Crop only the visual evidence needed by image-dependent chapter questions."""

from pathlib import Path

import fitz
from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "pdf" / "(PC다운로드용) [Lv2] Data Science 기본 교재.pdf"
OUTPUT = ROOT / "교재정리" / "images" / "questions"

# Normalized (left, top, right, bottom) crop boxes.  The crops deliberately
# exclude slide titles, question text, answer choices, and decorative headers.
CROPS = {
    "ch03_q04_boxplots.png": (97, (0.495, 0.275, 0.735, 0.875)),
    "ch09_q03_join_tables.png": (255, (0.465, 0.365, 0.985, 0.725)),
    "ch09_q05_sampling_tables.png": (259, (0.440, 0.315, 0.885, 0.795)),
    "ch11_q03_spearman.png": (314, (0.190, 0.300, 0.585, 0.765)),
    "ch11_q05_scatterplot.png": (318, (0.515, 0.310, 0.750, 0.900)),
    "ch12_q05_f1_table.png": (344, (0.440, 0.235, 0.630, 0.635)),
    "ch13_q04_vectors.png": (367, (0.315, 0.220, 0.600, 0.675)),
    "ch17_q04_knn_table.png": (471, (0.505, 0.305, 0.700, 0.700)),
    "ch18_q04_information_gain.png": (502, (0.265, 0.305, 0.615, 0.710)),
}


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    document = fitz.open(str(PDF))
    for filename, (page_number, box) in CROPS.items():
        pixmap = document[page_number - 1].get_pixmap(
            matrix=fitz.Matrix(2, 2), colorspace=fitz.csRGB, alpha=False
        )
        image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
        width, height = image.size
        left, top, right, bottom = box
        cropped = image.crop((
            int(left * width), int(top * height),
            int(right * width), int(bottom * height),
        ))
        # Remove blank slide canvas while retaining a small breathing margin.
        background = Image.new("RGB", cropped.size, "white")
        content_box = ImageChops.difference(cropped, background).getbbox()
        if content_box:
            padding = 12
            content_box = (
                max(0, content_box[0] - padding), max(0, content_box[1] - padding),
                min(cropped.width, content_box[2] + padding),
                min(cropped.height, content_box[3] + padding),
            )
            cropped = cropped.crop(content_box)
        target = OUTPUT / filename
        cropped.save(str(target), optimize=True)
        print("{} <- PDF {}".format(target, page_number))


if __name__ == "__main__":
    main()
