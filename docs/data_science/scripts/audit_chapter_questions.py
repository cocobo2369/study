"""Validate the 115 curated end-of-chapter questions and their links."""

import re
from pathlib import Path

from rebuild_chapter_questions import BANK, FILES, NOTES


BAD_OCR_TOKENS = [
    "확출", "관속", "주정", "정구분포", "제급", "문제 풀이 Q", "문제풀이 Q",
]


def github_slug(title):
    title = re.sub(r"<[^>]+>", "", title).strip().lower()
    title = re.sub(r"[`*_~]", "", title)
    title = re.sub(r"[^\w\-\s가-힣]", "", title, flags=re.UNICODE)
    return re.sub(r"\s+", "-", title).strip("-")


def main():
    errors = []
    total_questions = 0
    total_options = 0
    total_images = 0

    for chapter in range(1, 24):
        path = NOTES / FILES[chapter]
        text = path.read_text(encoding="utf-8")
        section_match = re.search(
            r"(?ms)^## \d+\. 교재 문제와 해설\s*\n(.*?)(?=^## )", text
        )
        if not section_match:
            errors.append("ch{:02d}: question section missing".format(chapter))
            continue
        section = section_match.group(1)
        blocks = re.split(r'(?=<a id="ch{:02d}-q\d+"></a>)'.format(chapter), section)
        blocks = [block for block in blocks if block.startswith('<a id="')]
        if len(blocks) != 5:
            errors.append("ch{:02d}: expected 5 blocks, got {}".format(chapter, len(blocks)))

        headings = re.findall(r"(?m)^### 문제 \d+\. ", section)
        details_open = section.count("<details>")
        details_close = section.count("</details>")
        if len(headings) != 5 or details_open != 5 or details_close != 5:
            errors.append(
                "ch{:02d}: headings/details = {}/{}/{}".format(
                    chapter, len(headings), details_open, details_close
                )
            )

        theory_headings = {
            github_slug(match.group(1))
            for match in re.finditer(r"(?m)^#{2,3}\s+(.+?)\s*$", text)
        }
        for question_number, block in enumerate(blocks, start=1):
            total_questions += 1
            before_details = block.split("<details>", 1)[0]
            options = re.findall(r"(?m)^([1-4])\.\s+(.+)$", before_details)
            expected_options = len(BANK[chapter][question_number - 1]["options"])
            if len(options) != expected_options:
                errors.append(
                    "ch{:02d} q{}: expected {} options, got {}".format(
                        chapter, question_number, expected_options, len(options)
                    )
                )
            total_options += len(options)

            rationales = re.findall(
                r"(?m)^- \*\*[①②③④] (?:정답|오답):\*\* .+$", block
            )
            if len(rationales) != expected_options:
                errors.append(
                    "ch{:02d} q{}: expected {} rationales, got {}".format(
                        chapter, question_number, expected_options, len(rationales)
                    )
                )
            if len(re.findall(r"(?m)^\*\*정답: [①②③④] .+\*\*$", block)) != 1:
                errors.append("ch{:02d} q{}: answer line count error".format(chapter, question_number))

            for anchor in re.findall(r"\]\(#([^)]+)\)", block):
                if anchor.startswith("ch{:02d}-q".format(chapter)):
                    continue
                if anchor not in theory_headings:
                    errors.append(
                        "ch{:02d} q{}: missing theory anchor #{}".format(
                            chapter, question_number, anchor
                        )
                    )

            for relative in re.findall(r"!\[[^]]*\]\(([^)]+)\)", block):
                total_images += 1
                if not (path.parent / relative).exists():
                    errors.append(
                        "ch{:02d} q{}: missing image {}".format(
                            chapter, question_number, relative
                        )
                    )

        for token in BAD_OCR_TOKENS:
            if token in section:
                errors.append("ch{:02d}: OCR token remains: {}".format(chapter, token))

    expected_options = 114 * 4 + 2
    print("chapters=23")
    print("questions={}".format(total_questions))
    print("options={} (expected {})".format(total_options, expected_options))
    print("question_images={}".format(total_images))
    print("errors={}".format(len(errors)))
    for error in errors:
        print("ERROR " + error)
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
