"""Turn an old Jinja + Markdown page into MDX for this site."""

import html
import re

from common import TERMS, load_links
from pagemap import HOMEWORK, PROJECTS, uses

OLD_TO_NEW = dict(TERMS)
PROJECT_USES = uses(PROJECTS)
HOMEWORK_USES = uses(HOMEWORK)
FILE_LINKS = load_links()

RETIRED_HOSTS = ("grader.cs465.byu.edu", "sebulba.cs.byu.edu", "167.172.158.71",
                 "cs465.byu.edu/project", "cs465.byu.edu/lab")
WORDLIST = "https://github.com/cracklib/cracklib/releases"


def extract(source: str) -> str:
    """The Markdown body of an old template."""
    m = re.search(r"\{%\s*filter markdown\s*%\}(.*?)\{%\s*endfilter\s*%\}", source, re.S)
    body = m.group(1) if m else source.split("{% block page %}", 1)[-1].split("{% endblock %}")[0]
    return re.sub(r"\{%.*?%\}", "", body, flags=re.S).strip("\n") + "\n"


# ---------------------------------------------------------------- links

def new_link(url: str, term: str, depth: int) -> str | None:
    """Map an old URL to a new one. None means: drop the link, keep the text."""
    url = re.sub(r"^(https?)://", lambda m: m.group(1).lower() + "://", url.strip(), flags=re.I)
    if any(h in url for h in RETIRED_HOSTS):
        return None
    if url.endswith("cracklib.txt"):
        return WORDLIST
    m = re.search(r"docs\.google\.com/(?:document|presentation)/d/([\w-]+)", url)
    if m and f"google:{m.group(1)}" in FILE_LINKS:
        return FILE_LINKS[f"google:{m.group(1)}"]
    path = re.sub(r"^https?://cs465(?:\.internet)?\.byu\.edu", "", url)
    if path in FILE_LINKS:
        target = FILE_LINKS[path]
        if target.startswith("@/images/"):
            return "../" * depth + "images/" + target.removeprefix("@/images/")
        return target
    m = re.match(r"^/?(?:([a-z]+-\d{4})/)?(projects|homework|help)/([\w.-]+?)(?:\.html)?/?(#.*)?$", path)
    if m:
        old_term, kind, name, anchor = m.groups()
        t = OLD_TO_NEW.get(old_term, term) if old_term else term
        anchor = anchor or ""
        if kind == "projects":
            slug = PROJECT_USES.get((t, name))
            return f"/crypto-course/projects/{slug}{anchor}" if slug else url
        if kind == "homework":
            slug = HOMEWORK_USES.get((t, name))
            return f"/crypto-course/homework/{slug}{anchor}" if slug else url
        if name.startswith("study-guide"):
            n = name[-1]
            if t == "winter2023":
                return None  # its study guides were never written ("TBD")
            if n == "1" and t in ("fall2018", "fall2019"):
                return "/crypto-course/study-guides/midterm-1-2018"
            return f"/crypto-course/study-guides/midterm-{n}"
        return f"/{t}/staff"
    m = re.match(r"^/?([a-z]+-\d{4})/?(.*)$", path)
    if m and m.group(1) in OLD_TO_NEW:
        rest = m.group(2)
        if rest in ("", "schedule"):
            return f"/{OLD_TO_NEW[m.group(1)]}"
        if rest == "lectures":
            return "/crypto-course/lectures"
    return url


def rewrite_links(text: str, term: str, depth: int, report: list) -> str:
    # <img src="..." ...> -> Markdown image (Astro optimizes these)
    text = re.sub(r'<img\s[^>]*?src="?([^"\s>]+)"?[^>]*?(?:alt="([^"]*)")?[^>]*>',
                  lambda m: f"![{m.group(2) or ''}]({m.group(1)})", text, flags=re.I)
    def md(m):
        label, url = m.group(1), m.group(2)
        new = new_link(url, term, depth)
        if new is None:
            report.append(f"retired link: {url}")
            if label.startswith("http"):
                return f"`{label}` (retired)"
            return f"{label} (retired: `{url}`)"
        if new == url and url.startswith("/"):
            report.append(f"UNMAPPED link: {url}")
        bang = "!" if m.group(0).startswith("!") else ""
        return f"{bang}[{label}]({new})"
    # bare URLs to retired graders (not ones inside Markdown links)
    for host in RETIRED_HOSTS:
        text = re.sub(r"(?<![(\[/`])(https?://" + re.escape(host) + r"[^\s)\]`]*)", r"`\1` (retired)", text)
    text = re.sub(r"!?\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)", md, text)
    return text


# ---------------------------------------------------------------- MDX safety

FENCE = re.compile(r"^(\s*)(```|~~~)")
LIST_ITEM = re.compile(r"^\s*([*+-]|\d+\.)\s+")


def fence_code(lines: list[str]) -> list[str]:
    """MDX has no indented code blocks: fence them. <pre> blocks too."""
    out, i, in_list, in_fence = [], 0, False, False
    while i < len(lines):
        line = lines[i]
        if FENCE.match(line):
            in_fence = not in_fence
            out.append(line.strip() if not in_list else line)
            i += 1
            continue
        if in_fence:
            out.append(line); i += 1; continue
        if line.strip().lower().startswith("<pre"):
            block = [re.sub(r"(?i)^\s*<pre[^>]*>", "", line)]
            while "</pre>" not in block[-1].lower() and i + 1 < len(lines):
                i += 1
                block.append(lines[i])
            block[-1] = re.sub(r"(?i)</pre>.*", "", block[-1])
            block = [html.unescape(re.sub(r"</?code[^>]*>", "", b)) for b in block]
            while block and not block[0].strip(): block.pop(0)
            while block and not block[-1].strip(): block.pop()
            out += ["", "```", *block, "```", ""]
            i += 1
            continue
        if LIST_ITEM.match(line):
            in_list = True
        elif line.strip() and not line.startswith((" ", "\t")):
            in_list = False
        prev_blank = not out or not out[-1].strip()
        if not in_list and prev_blank and re.match(r"^( {4}|\t)\S", line):
            block = []
            while i < len(lines) and (re.match(r"^( {4}|\t)", lines[i]) or not lines[i].strip()):
                block.append(re.sub(r"^( {4}|\t)", "", lines[i]))
                i += 1
            while block and not block[-1].strip(): block.pop()
            out += ["```", *block, "```", ""]
            continue
        out.append(line)
        i += 1
    return out


INLINE_TAGS = [(r"</?(b|strong)>", "**"), (r"</?(i|em)>", "*"), (r"<br\s*/?>", "<br />"),
               (r"</?p>", "\n"), (r"</?font[^>]*>", ""), (r"</?center>", ""), (r"</?u>", "")]


def escape_text(text: str, math: bool) -> str:
    """Escape what MDX would read as JSX or expressions, outside code and math."""
    protected = r"(`[^`\n]+`)"
    if math:
        protected = r"(\$\$.*?\$\$|\$[^$\n]+\$|`[^`\n]+`)"
    parts = re.split(protected, text, flags=re.S)
    for k in range(1, len(parts), 2):
        if parts[k].startswith("$"):  # % starts a comment in TeX
            parts[k] = re.sub(r"(?<!\\)%", r"\\%", parts[k])
    for k in range(0, len(parts), 2):
        s = parts[k]
        s = re.sub(r"<!--(.*?)-->", lambda m: "{/*" + m.group(1).replace("*/", "* /") + "*/}", s, flags=re.S)
        for pat, rep in INLINE_TAGS:
            s = re.sub(pat, rep, s, flags=re.I)
        s = re.sub(r"(?<![{])\{(?!/\*)", r"\\{", s)
        s = re.sub(r"(?<!\*/)\}", r"\\}", s)
        s = re.sub(r"<(?!br />|/?(a|img|sup|sub|table|thead|tbody|tr|td|th|ul|ol|li|div|span|code)\b)", "&lt;", s)
        if not math:
            s = s.replace("$", "\\$")
        parts[k] = s
    return "".join(parts)


def display_math(text: str) -> str:
    """A paragraph that is only $$...$$ is a display equation; remark-math
    wants the delimiters on their own lines for that."""
    return re.sub(r"^[ \t]*\$\$(.+?)\$\$[ \t]*$", lambda m: "$$\n" + m.group(1).strip() + "\n$$",
                  text, flags=re.M)


def to_mdx(markdown: str, term: str, depth: int, math: bool, report: list) -> str:
    if math:
        markdown = display_math(markdown)
    lines = fence_code(markdown.replace("\r\n", "\n").expandtabs(4).split("\n"))
    out, chunk, in_fence = [], [], False

    def flush():
        if chunk:
            out.append(escape_text(rewrite_links("\n".join(chunk), term, depth, report), math))
            chunk.clear()

    for line in lines:
        if FENCE.match(line):
            if not in_fence:
                flush()
            else:
                out.append("\n".join(chunk)); chunk.clear()
            in_fence = not in_fence
            out.append(line)
        else:
            chunk.append(line)
    flush()
    text = "\n".join(out)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
