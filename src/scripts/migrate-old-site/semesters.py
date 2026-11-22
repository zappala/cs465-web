"""Write each 2018-2023 semester's menu, schedule page, staff and syllabus.

The rendered 2022 pages need markdownify:
  uv run --with markdownify python semesters.py
"""

import re

from common import OLD, TERMS, WEB
from convert import extract, to_mdx
from menus import quote
from pagemap import HOMEWORK, NAMES, PROJECTS, uses

PROJECT_USES = uses(PROJECTS)
HOMEWORK_USES = uses(HOMEWORK)
RENDERED = {"winter2022", "spring2022"}

# Names and roles only (decided 2026-11-21: no photos, contact details or
# office hours). From each semester's "Instructor and TAs" page.
STAFF = {
    "fall2018": ("Daniel Zappala", "Associate Professor", []),
    "winter2019": ("Fred Clift", "Adjunct Professor", ["Nathan Black", "Mike Liddle", "Garrett Wilhelm"]),
    "fall2019": ("Daniel Zappala", "Professor", []),
    "winter2020": ("Fred Clift", "Adjunct Professor", ["Tyler Brady"]),
    "fall2020": ("Fred Clift", "Adjunct Professor", ["Bryce Pierson", "Trevin Avery"]),
    "fall2021": ("Fred Clift", "Adjunct Professor", ["Bryce Pierson", "Paul Spencer"]),
    "winter2022": ("Brett Decker", "Assistant Professor", ["Travis Feller"]),
    "spring2022": ("Tarun Kumar Yadav", "PhD Student", ["Travis Feller"]),
    "fall2022": ("Fred Clift", "Adjunct Professor", ["Travis Feller", "Ben Grant"]),
    "winter2023": ("James Conners", "PhD Student", ["Joshua Esplin", "Benjamin Grant"]),
    "fall2023": ("Fred Clift", "Adjunct Professor", ["Josh Esplin"]),
}


def old_page(term_old, rel):
    base = OLD / "templates" / term_old
    for p in (base / f"{rel}.html", base / rel):
        if p.exists():
            return p.read_text()
    return None


def menu_entries(term_old, term):
    """(kind, old name, label) in the order of the old menu."""
    if term in RENDERED:
        page = old_page(term_old, "index")
        nav = page[page.find("navbarSupportedContent"):page.find("</nav>")]
        found = re.findall(rf'href="?/{term_old}/(projects|homework|help)/([\w.-]+)"?\s*>\s*([^<]+?)\s*<', nav)
    else:
        menu = old_page(term_old, "menu")
        found = [(d or "help", n.split("/")[-1], label) if "/" not in n else (n.split("/")[0], n.split("/")[1], label)
                 for d, n, label in re.findall(r"dropdown\('([^']*)','([^']*)','([^']*)'\)", menu)]
    return found


def write_menu(term_old, term):
    projects, homework, guides = [], [], []
    for kind, name, label in menu_entries(term_old, term):
        if kind == "projects" and (term, name) in PROJECT_USES:
            projects.append((label, f"/crypto-course/projects/{PROJECT_USES[(term, name)]}"))
        elif kind == "homework" and (term, name) in HOMEWORK_USES:
            slug = HOMEWORK_USES[(term, name)]
            if re.fullmatch(r"Homework #[\d.]+", label):
                label += f": {HOMEWORK[slug][0]}"
            homework.append((label, f"/crypto-course/homework/{slug}"))
        elif kind == "help" and name.startswith("study-guide") and term != "winter2023":
            n = name[-1]
            slug = f"midterm-{n}-2018" if (n == "1" and term in ("fall2018", "fall2019")) else f"midterm-{n}"
            guides.append((label, f"/crypto-course/study-guides/{slug}"))
    lines = ["menu:", f"  semester: {NAMES[term]}", "  items:",
             "    - title: Home", "      url: /",
             "    - title: Syllabus", "      url: /syllabus",
             "    - title: Staff", "      url: /staff"]
    for title, items in (("Projects", projects), ("Homework", homework), ("Exams", guides)):
        if items:
            lines += [f"    - title: {title}", "      submenu:"]
            for label, url in items:
                lines += [f"        - title: {quote(label)}", f"          url: {url}"]
    lines += ["    - title: Lectures", "      url: /crypto-course/lectures",
              "    - title: Overview", "      url: /crypto-course"]
    (WEB / "src/data" / term / "menu.yaml").write_text("\n".join(lines) + "\n")
    return len(projects), len(homework), len(guides)


NOTICE = """<Notice title="2018–2023 course">
  This is an archived semester of the cryptography-focused course taught
  from 2018 to 2023. Projects, homework and slides are shared by several
  semesters; see the [overview](/crypto-course) for all of them. The
  course was reorganized in 2024; see the [home page](/) for the current
  course.
</Notice>"""


def write_index(term):
    page = f"""---
layout: ../../layouts/Semester.astro
title: Schedule
---

import GridSchedule from "../../components/GridSchedule.jsx";
import Notice from "../../components/Notice.jsx";

<article
    class="prose prose-blockquote:not-italic prose-blockquote:font-normal prose-blockquote:text-base prose-blockquote:bg-blue-200 prose-blockquote:border-l-0 prose-blockquote:px-4 prose-blockquote:py-1 prose-blockquote:rounded-lg pb-8 text-lg">

# Schedule

{NOTICE}

</article>

<GridSchedule prefix="/{term}" />
"""
    (WEB / "src/pages" / term).mkdir(parents=True, exist_ok=True)
    (WEB / "src/pages" / term / "index.mdx").write_text(page)


def write_staff(term):
    name, role, tas = STAFF[term]
    ta_text = "\n".join(f"- {t}" for t in tas) if tas else "Not listed."
    page = f"""---
layout: ../../layouts/CryptoCourseMarkdown.astro
---

# Staff

## Instructor

{name}, {role}

## Teaching assistants

{ta_text}
"""
    (WEB / "src/pages" / term / "staff.mdx").write_text(page)


def write_syllabus(term_old, term):
    report = []
    source = old_page(term_old, "index")
    if term in RENDERED:
        from markdownify import markdownify
        body_html = source[source.find('id="page"'):]
        body_html = body_html[body_html.find(">") + 1:]
        body_html = re.split(r"<script|MathJax", body_html)[0]
        markdown = markdownify(body_html, heading_style="ATX", bullets="*")
    else:
        markdown = extract(source)
    body = to_mdx(markdown, term, depth=2, math=False, report=report)
    body = re.sub(r"^(#{1,4})(?=[^#\s])", r"\1 ", body, flags=re.M)
    page = f"""---
layout: ../../layouts/CryptoCourseMarkdown.astro
title: Syllabus
---

{body}"""
    (WEB / "src/pages" / term / "syllabus.mdx").write_text(page)
    for line in sorted(set(report)):
        print(f"  {term}/syllabus: {line}")


if __name__ == "__main__":
    for term_old, term in TERMS:
        counts = write_menu(term_old, term)
        write_index(term)
        write_staff(term)
        write_syllabus(term_old, term)
        print(f"{term}: menu has {counts[0]} projects, {counts[1]} homework, {counts[2]} study guides")
