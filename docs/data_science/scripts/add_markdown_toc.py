"""Insert or refresh a local table of contents in all 23 chapter notes."""

from pathlib import Path
import re


START = "<!-- TOC START -->"
END = "<!-- TOC END -->"


def locate_notes_dir():
    return next(
        path.parent
        for path in Path(".").glob("*/*.md")
        if path.name == "README.md"
        and len(list(path.parent.glob("[0-9][0-9]_*.md"))) == 23
    )


def github_slug(title, used):
    title = re.sub(r"<[^>]+>", "", title).strip().lower()
    title = re.sub(r"[`*_~]", "", title)
    title = re.sub(r"[^\w\-\s가-힣]", "", title, flags=re.UNICODE)
    slug = re.sub(r"\s+", "-", title).strip("-")
    count = used.get(slug, 0)
    used[slug] = count + 1
    return slug if count == 0 else f"{slug}-{count}"


def strip_existing_toc(text):
    pattern = re.compile(
        rf"\n?{re.escape(START)}.*?{re.escape(END)}\n?", re.DOTALL
    )
    text = pattern.sub("\n", text)
    return re.sub(r"\n{3,}", "\n\n", text)


def build_toc(text):
    used = {}
    entries = []
    for line in text.splitlines():
        match = re.match(r"^(#{1,3})\s+(.+?)\s*$", line)
        if not match:
            continue
        level = len(match.group(1))
        title = match.group(2)
        if title in {"주요 단어 먼저 보기", "목차"}:
            continue
        slug = github_slug(title, used)
        if level == 1:
            continue
        indent = "  " * (level - 2)
        entries.append(f"{indent}- [{title}](#{slug})")
    return "\n".join(entries)


def insert_toc(text, toc):
    lines = text.splitlines()
    insert_at = 1
    keyword_at = next(
        (index for index, line in enumerate(lines) if line == "## 주요 단어 먼저 보기"),
        None,
    )
    if keyword_at is not None:
        # The keyword glossary must always be the first unit content.
        insert_at = next(
            (
                index
                for index, line in enumerate(lines[keyword_at + 1 :], start=keyword_at + 1)
                if re.match(r"^## (?:\d+\.|시험|보충|추가)", line)
            ),
            len(lines),
        )
    else:
        for index, line in enumerate(lines[1:], start=1):
            if line.startswith("> 원본 PDF 범위:"):
                insert_at = index + 1
                break
    block = ["", START, "## 목차", "", toc, END, ""]
    lines[insert_at:insert_at] = block
    return "\n".join(lines).rstrip() + "\n"


def main():
    notes_dir = locate_notes_dir()
    files = sorted(notes_dir.glob("[0-9][0-9]_*.md"))
    for path in files:
        text = strip_existing_toc(path.read_text(encoding="utf-8"))
        path.write_text(insert_toc(text, build_toc(text)), encoding="utf-8")
    print(f"Updated TOCs in {len(files)} chapter files")


if __name__ == "__main__":
    main()
