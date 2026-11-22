"""Shared pages other than projects and homework: the lectures page and the
study guides."""

import re
from collections import defaultdict

from common import LECTURE_DIRS, OLD, WEB, load_links
from convert import extract, to_mdx

OUT = WEB / "src/pages/crypto-course"
HEADER = """---
layout: ../../layouts/CryptoCourseMarkdown.astro
---

import UsedIn from "../../components/UsedIn.jsx";
"""
SUB_HEADER = HEADER.replace("../../", "../../../")


def template(term, rel):
    return (OLD / "templates" / term / rel).read_text()


def lectures():
    """The Fall 2023 'Lectures and other Resources' page, plus every slide deck."""
    source = template("fall-2023", "lectures.html")
    source = re.sub(r"\{#.*?#\}", "", source, flags=re.S)
    source = source.replace("{{base}}../../pubs/", "/static/pubs/").replace("{{base}}", "/static/lectures/f23")
    report = []
    body = to_mdx(extract(source), "fall2023", depth=2, math=False, report=report)
    body = re.sub(r"^#\s*Lectures.*\n", "", body.lstrip(), count=1)
    body = re.sub(r"^(#{2,3})(?=\S)", r"\1 ", body, flags=re.M)  # "##Course" -> "## Course"

    used = defaultdict(list)  # new pdf -> semesters
    for old, new in load_links().items():
        m = re.match(r"/static/lectures/(\w+)/", old)
        if m:
            used[new].append(m.group(1))
    order = [folder for folder, _ in LECTURE_DIRS]
    rows = []
    for new in sorted(used):
        sems = sorted(set(used[new]), key=order.index)
        rows.append(f"| [{new.rsplit('/', 1)[1]}]({new}) | {', '.join(sems)} |")
    DOCS = "/lectures/crypto-course/docs"
    page = HEADER + f"""
# Lectures and Other Resources

<UsedIn>This is the Fall 2023 page. Earlier semesters had a similar page
listing their own folder of slides; all versions of the slides are in the
table at the end.</UsedIn>

{body}
## Earlier versions

Winter 2019 to Fall 2023 had this page (Fall 2018 and Fall 2019 didn't);
each linked its own semester's slide folder. Otherwise:

- Winter 2019 and Winter 2020 linked the older [TLS slides](/lectures/crypto-course/TLS.pdf)
  instead of [TLS-2020](/lectures/crypto-course/TLS-2020.pdf).
- Winter 2022 and Spring 2022 also linked Wikipedia's
  [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) article and
  [Please Stop Encrypting with RSA Directly](https://soatok.blog/2021/01/20/please-stop-encrypting-with-rsa-directly/),
  and their own study guides
  ([Midterm 1]({DOCS}/midterm-1-study-guide-winter2022.pdf),
  [Midterm 2]({DOCS}/midterm-2-study-guide-winter2022.pdf)).

## All slide decks

Every slide deck from Fall 2018 to Fall 2023, once each. Where a deck
changed, the file name ends with the first semester that used that
version. The second column lists the old site's slide folders that had a
copy: `v1` (Fall 2018 and Fall 2019), `v2` (Fall 2019), then `w19`,
`w20`, `f20`, `f21`, `f22`, `f23` for each semester. Winter 2022 and
Spring 2022 used the `f21` folder.

| Slides | Old folders |
| --- | --- |
""" + "\n".join(rows) + "\n"
    (OUT / "lectures.mdx").write_text(page)
    for line in sorted(set(report)):
        print("  lectures:", line)


def study_guide(name, term, rel, used_in, notes=""):
    report = []
    body = to_mdx(extract(template(term, rel)), term.replace("-", ""), depth=3, math=False, report=report)
    body = re.sub(r"^(#{1,3})(?=\S)", r"\1 ", body, flags=re.M)
    body = re.sub(r"^#\s.*\n", "", body.lstrip(), count=1) if body.lstrip().startswith("# ") else body
    title = {"midterm-1-2018": "Midterm 1 Study Guide (Fall 2018 and Fall 2019)",
             "midterm-1": "Midterm 1 Study Guide", "midterm-2": "Midterm 2 Study Guide"}[name]
    page = SUB_HEADER + f"\n# {title}\n\n<UsedIn>{used_in}</UsedIn>\n\n{notes}{body}"
    (OUT / "study-guides").mkdir(parents=True, exist_ok=True)
    (OUT / "study-guides" / f"{name}.mdx").write_text(page)
    for line in sorted(set(report)):
        print(f"  study-guides/{name}:", line)


DOCS = "/lectures/crypto-course/docs"

INSTRUCTORS = {"fall2018": "Daniel Zappala", "winter2019": "Fred Clift", "fall2019": "Daniel Zappala",
               "winter2020": "Fred Clift", "fall2020": "Fred Clift", "fall2021": "Fred Clift",
               "winter2022": "Brett Decker", "spring2022": "Tarun Kumar Yadav", "fall2022": "Fred Clift",
               "winter2023": "James Conners", "fall2023": "Fred Clift"}


def overview():
    from pagemap import ALL, HOMEWORK, NAMES, PROJECTS, terms

    def span(rows):
        used = sorted({t for spec, _, _ in rows for t in terms(spec)}, key=ALL.index)
        return "all semesters" if len(used) == len(ALL) else (
            NAMES[used[0]] if len(used) == 1 else f"{NAMES[used[0]]} to {NAMES[used[-1]]}")

    def listing(kind, table):
        return "\n".join(f"- [{title}](/crypto-course/{kind}/{slug}) ({span(rows)})"
                          for slug, (title, rows) in table.items())

    semesters = "\n".join(f"| [{NAMES[t]}](/{t}) | {INSTRUCTORS[t]} |" for t in reversed(ALL))
    page = """---
layout: ../../layouts/CryptoCourseMarkdown.astro
title: 2018–2023 Course
---

# CS 465 from 2018 to 2023

From Fall 2018 to Fall 2023, CS 465 was a cryptography-focused course.
The course was reorganized in 2024; see the [home page](/) for the
current course. This section keeps every project, homework, study guide
and slide deck from those years, once each. Each page says which
semesters used it and under which number.

The course description from that time:

> This course covers fundamental principles of computer security. The
> course consists of three parts:
>
> **Part 1: Cryptography:** We will study and experiment with basic
> cryptographic primitives (symmetric encryption, asymmetric encryption,
> MAC, and cryptographic hash functions). We will learn how these
> primitives are used to achieve certain security properties.
>
> **Part 2: Systems:** We will study systems that use cryptography,
> including HTTPS and secure email, to see how cryptographic primitives are
> used in practice on the Internet.
>
> **Part 3: Software Security:** We will learn about some of the most
> common errors that software developers make that attackers then
> exploit. We will learn how to avoid or prevent these mistakes.
>
> Prerequisite: CS 324 (concurrent) or instructor consent.

## Semesters

Each semester has its schedule, syllabus and staff, linking to the pages
below.

| Semester | Instructor |
| --- | --- |
""" + semesters + """

## Projects

""" + listing("projects", PROJECTS) + """

The project graders (on `grader.cs465.byu.edu` and earlier sites) were
retired with the course.

## Homework

""" + listing("homework", HOMEWORK) + """

## Study guides and slides

- [Midterm 1 study guide, Fall 2018 and Fall 2019](/crypto-course/study-guides/midterm-1-2018)
- [Midterm 1 study guide, Winter 2019 to Fall 2023](/crypto-course/study-guides/midterm-1)
- [Midterm 2 study guide](/crypto-course/study-guides/midterm-2)
- [Lectures and other resources](/crypto-course/lectures), with every slide deck
"""
    (OUT / "index.mdx").write_text(page)

if __name__ == "__main__":
    overview()
    lectures()
    study_guide("midterm-1-2018", "fall-2018", "help/study-guide-midterm1.html",
                "[Fall 2018](/fall2018), [Fall 2019](/fall2019)")
    study_guide("midterm-1", "fall-2023", "help/study-guide-midterm1.html",
                "[Winter 2019](/winter2019) to [Fall 2023](/fall2023), except Fall 2019 and Winter 2023",
                f"""From Winter 2019 on this page mostly held exam logistics; the topics
moved to a separate document. Saved copies:
[Winter 2022]({DOCS}/midterm-1-study-guide-winter2022.pdf),
[Fall 2023]({DOCS}/midterm-1-study-guide-fall2023.pdf). Exam dates and
places differed each semester; this is the Fall 2023 page.

""")
    study_guide("midterm-2", "fall-2023", "help/study-guide-midterm2.html",
                "[Fall 2018](/fall2018) to [Fall 2023](/fall2023), except Winter 2023",
                f"""The topics list below was the same every semester (Fall 2019 and the
2022 semesters had small wording changes). Later semesters also had a
separate document: [Winter 2022]({DOCS}/midterm-2-study-guide-winter2022.pdf),
[Fall 2023]({DOCS}/midterm-2-study-guide-fall2023.pdf).

""")
    print("done")
