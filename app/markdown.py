import re


_TABLE_RE = re.compile(r"<table[^>]*>(.*?)</table>", re.DOTALL | re.IGNORECASE)
_TR_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_CELL_RE = re.compile(r"<(th|td)[^>]*>(.*?)</\1>", re.DOTALL | re.IGNORECASE)


def _cell_text(raw: str) -> str:
    raw = re.sub(r"<br\s*/?>", " ", raw, flags=re.IGNORECASE)
    raw = re.sub(r"<[^>]+>", "", raw)
    raw = raw.replace("|", r"\|")
    return " ".join(raw.split())


def _table_to_markdown(inner_html: str) -> str:
    rows = []
    for tr in _TR_RE.finditer(inner_html):
        cells = [_cell_text(m.group(2)) for m in _CELL_RE.finditer(tr.group(1))]
        if cells and any(c for c in cells):
            rows.append(cells)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    header, body = rows[0], rows[1:]
    lines = ["| " + " | ".join(header) + " |",
             "| " + " | ".join(["---"] * width) + " |"]
    for r in body:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def convert_html_tables(text: str) -> str:
    return _TABLE_RE.sub(lambda m: "\n\n" + _table_to_markdown(m.group(1)) + "\n\n", text)


def strip_html(text: str) -> str:
    clean = re.sub(r"<[^>]+>", "", text)
    return clean


def strip_image_tags(text: str) -> str:
    return re.sub(r"!\[.*?\]\(.*?\)\n*", "", text)
