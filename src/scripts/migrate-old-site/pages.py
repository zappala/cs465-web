"""Write the shared project and homework pages from the newest old version."""

import re
import sys

from common import OLD, TERMS, WEB
from convert import extract, to_mdx
from notes import NOTES
from pagemap import ALL, HOMEWORK, NAMES, PROJECTS, terms

NEW_TO_OLD = {new: old for old, new in TERMS}
OUT = WEB / "src/pages/crypto-course"
MATH = {("projects", "diffie-hellman"), ("projects", "rsa"), ("homework", "rsa-keys")}


def runs(term_list):
    """Group terms into runs of consecutive semesters."""
    idx = sorted(ALL.index(t) for t in set(term_list))
    groups, start = [], idx[0]
    for a, b in zip(idx, idx[1:] + [None]):
        if b != a + 1:
            groups.append((ALL[start], ALL[a]))
            start = b
    return groups


def used_in(kind, rows):
    label = "Project" if kind == "projects" else "Homework"
    parts = []
    for spec, _old, number in rows:
        when = ", ".join(f"[{NAMES[a]}](/{a})" if a == b else f"[{NAMES[a]}](/{a}) to [{NAMES[b]}](/{b})"
                         for a, b in runs(terms(spec)))
        parts.append(f"{when} (as {label} {number})" if number else f"{when} (as an extra page)")
    return "; ".join(parts)


def old_file(term, kind, name):
    base = OLD / "templates" / NEW_TO_OLD[term] / kind
    for candidate in (base / f"{name}.html", base / name):
        if candidate.exists():
            return candidate
    raise FileNotFoundError(base / name)


def earlier_versions(kind, slug, report):
    """The 'Earlier versions' section, if the page changed over time."""
    if slug == "social-engineering":
        old = to_mdx(extract(old_file("fall2021", "homework", "homework98").read_text()), "fall2021",
                     depth=3, math=False, report=report)
        old = re.sub(r"^#\s.*\n", "", old.lstrip(), count=1)
        return f"""
## Earlier versions

- Fall 2020 to Fall 2022 asked students to "at least attempt the attack
  phase" rather than "complete all phases".
- In Winter 2022 and Spring 2022 the target was that semester's instructor
  (Brett Decker, Tarun Kumar Yadav), with "guidance from Prof. Clift that
  applies generally".
- Winter 2019 to Fall 2021 used a shorter version (as Homework 13, and as an
  extra page):

<details>
<summary>The Winter 2019 to Fall 2021 version</summary>

{old}
</details>
"""
    if slug in NOTES:
        return "\n## Earlier versions\n" + NOTES[slug]
    return ""


def write(kind, slug, title, rows):
    newest = max(((t, old) for spec, old, _ in rows for t in terms(spec)), key=lambda x: ALL.index(x[0]))
    term, name = newest
    report = []
    body = to_mdx(extract(old_file(term, kind, name).read_text()), term, depth=3,
                  math=(kind, slug) in MATH, report=report)
    body = re.sub(r"^#\s.*\n", "", body.lstrip(), count=1)  # old numbered title
    label = "Project" if kind == "projects" else "Homework"
    page = f"""---
layout: ../../../layouts/CryptoCourseMarkdown.astro
---

import UsedIn from "../../../components/UsedIn.jsx";

# {label}: {title}

<UsedIn>{used_in(kind, rows)}</UsedIn>

{body}"""
    page += earlier_versions(kind, slug, report)
    path = OUT / kind / f"{slug}.mdx"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page)
    for line in sorted(set(report)):
        print(f"  {kind}/{slug}: {line}")


if __name__ == "__main__":
    only = sys.argv[1:]
    for kind, table in (("projects", PROJECTS), ("homework", HOMEWORK)):
        for slug, (title, rows) in table.items():
            if not only or slug in only:
                write(kind, slug, title, rows)
    print("done")
