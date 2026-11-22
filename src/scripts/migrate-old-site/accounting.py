"""Check that every old page is accounted for: where it went, or why not."""

import os
from collections import Counter

from common import OLD, TERMS
from pagemap import HOMEWORK, PROJECTS, uses

P, H = uses(PROJECTS), uses(HOMEWORK)
OLD_TO_NEW = dict(TERMS)
DROPPED = {
    "help/officehours": "dropped: office hours (decision: names and roles only)",
    "help/slack": "dropped: Slack invitation (dead link)",
    "help/tarun_photo.jpg": "dropped: staff photo (decision)",
    "menu": "-> menu.yaml",
    "save": "dropped: a test page with one link",
    "misc": "-> its one link is the John/hashcat tutorial page",
}


def where(term, rel):
    name = rel.removesuffix(".html")
    kind, _, base = name.partition("/")
    if kind == "projects" and (term, base) in P:
        return f"-> crypto-course/projects/{P[(term, base)]}"
    if kind == "homework" and (term, base) in H:
        return f"-> crypto-course/homework/{H[(term, base)]}"
    if name.startswith("help/study-guide"):
        return "dropped: 'TBD' placeholder" if term == "winter2023" else "-> crypto-course/study-guides"
    if name == "help/instructor":
        return f"-> {term}/staff"
    if name == "index":
        return f"-> {term}/syllabus"
    if name == "schedule":
        return f"-> {term} schedule.yaml"
    if name == "lectures":
        return "-> crypto-course/lectures"
    return DROPPED.get(name, "UNACCOUNTED")


if __name__ == "__main__":
    tally = Counter()
    for term_old, term in TERMS:
        for dp, _, files in os.walk(OLD / "templates" / term_old):
            for f in files:
                rel = os.path.relpath(os.path.join(dp, f), OLD / "templates" / term_old)
                dest = where(term, rel)
                tally[dest.split(" ")[0] + " " + dest.split(" ")[1].split("/")[0]] += 1
                if dest == "UNACCOUNTED":
                    print("UNACCOUNTED:", term_old, rel)
    for k, v in sorted(tally.items()):
        print(f"{v:4}  {k}")
    print(sum(tally.values()), "old page files")
