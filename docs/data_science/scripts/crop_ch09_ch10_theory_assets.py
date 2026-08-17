"""Crop only the explanatory figures needed by chapters 9 and 10.

The source pages are rendered from the textbook PDF first.  This script removes
the surrounding slide chrome, headings, and prose so the Markdown files embed
the figures themselves rather than whole slides.
"""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "교재정리" / "_audit" / "rendered_pages"
OUTPUT = ROOT / "교재정리" / "images"


CROPS = {
    "ch09_outlier_detection.png": (235, (175, 465, 1940, 890)),
    "ch09_probability_sampling_methods.png": (246, (175, 465, 1665, 825)),
    "ch10_power_transform_example.png": (264, (175, 285, 1940, 865)),
    "ch10_log_transform_example.png": (266, (175, 285, 1940, 865)),
    "ch10_minmax_example.png": (269, (175, 285, 1940, 865)),
    "ch10_standardization_example.png": (271, (175, 285, 1940, 865)),
    "ch10_onehot_example.png": (273, (175, 690, 1845, 1020)),
}


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for name, (page, box) in CROPS.items():
        source = SOURCE / f"page_{page:03d}.png"
        if not source.exists():
            raise FileNotFoundError(f"Render PDF page {page} first: {source}")
        with Image.open(source) as image:
            cropped = image.crop(box)
            target = OUTPUT / name
            cropped.save(target, optimize=True)
            print(f"{target.relative_to(ROOT)} {cropped.size}")


if __name__ == "__main__":
    main()
