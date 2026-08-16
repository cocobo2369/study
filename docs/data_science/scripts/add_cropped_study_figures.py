from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "교재정리" / "_audit" / "figure_candidates"
IMAGES = ROOT / "교재정리" / "images"


CROPS = {
    "population_sample_flow.png": ("p007.png", (115, 245, 1135, 860)),
    "skewness_positions.png": ("p051.png", (610, 315, 1290, 650)),
    "boxplot_anatomy.png": ("p084.png", (145, 475, 1050, 895)),
    "bernoulli_shapes.png": ("p164.png", (610, 355, 1335, 720)),
    "chi_square_family.png": ("p193.png", (145, 535, 760, 900)),
    "clt_sample_means.png": ("p211.png", (615, 385, 1145, 830)),
}


INSERTIONS = [
    ("01_통계분석개요.md", "## 3. 관련 기호", "population_sample_flow.png", "모집단에서 표본을 뽑고, 표본 통계량으로 모집단 모수를 추론하는 관계"),
    ("02_통계량.md", "## 6. 통계량의 선형 연산", "skewness_positions.png", "왜도에 따른 평균·중앙값·최빈값의 상대적 위치"),
    ("03_자료의_표현.md", "## 6. 이변량 그래프", "boxplot_anatomy.png", "상자그림의 사분위수·IQR·수염 구조"),
    ("06_이산확률분포.md", "## 4. 이항분포", "bernoulli_shapes.png", "성공확률에 따른 베르누이 분포의 모양"),
    ("07_연속확률분포.md", "## 보충 학습", "chi_square_family.png", "자유도에 따라 달라지는 카이제곱분포의 모양"),
    ("08_추론통계.md", "## 4. 표본분포", "clt_sample_means.png", "표본크기가 커질수록 표본평균 분포가 정규분포에 가까워지는 모습"),
]


def crop_figures() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    for output_name, (source_name, box) in CROPS.items():
        with Image.open(CANDIDATES / source_name) as source:
            source.crop(box).save(IMAGES / output_name, optimize=True)


def insert_before(text: str, marker: str, block: str) -> str:
    if block.strip() in text:
        return text
    index = text.find(marker)
    if index < 0:
        raise ValueError(f"삽입 기준을 찾지 못함: {marker}")
    return text[:index].rstrip() + "\n\n" + block + "\n\n" + text[index:]


def add_links() -> None:
    notes = ROOT / "교재정리"
    for filename, next_heading, image_name, caption in INSERTIONS:
        path = notes / filename
        text = path.read_text(encoding="utf-8")
        block = f"![{caption}](images/{image_name})\n\n*그림: {caption} — 원문 슬라이드에서 설명에 필요한 도해 영역만 잘라 수록.*"
        path.write_text(insert_before(text, next_heading, block), encoding="utf-8")


if __name__ == "__main__":
    crop_figures()
    add_links()
