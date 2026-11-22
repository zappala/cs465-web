"""Convert the old Python schedules (views/<term>.py) to schedule.yaml."""

import datetime
import importlib
import re
import sys
import types

from common import OLD, TERMS, WEB
from convert import new_link
from pagemap import HOMEWORK, PROJECTS, uses

PROJECT_USES = uses(PROJECTS)
HOMEWORK_USES = uses(HOMEWORK)


# ------------------------------------------------ stand-ins for the old code

class Day:
    def __init__(self, date):
        self.date, self.lectures, self.readings, self.slides, self.assignments = date, [], [], [], []

    def lecture(self, section, topic=None):
        self.lectures.append(section + (f": {topic}" if topic else ""))

    def reading(self, text, link=None):
        self.readings.append((text, link))

    def slide(self, text, link=None):
        self.slides.append((text, link))

    def assignment(self, text, link=None):
        self.assignments.append((text, link))


class Schedule:
    def __init__(self):
        self.weeks = []

    def week(self):
        self.weeks.append([])

    def day(self, date):
        d = Day(date)
        self.weeks[-1].append(d)
        return d


def load(term_old):
    """Run views/<term>.py's schedule function and return its Schedule."""
    flask = types.ModuleType("flask")
    flask.render_template = lambda *a, **k: k
    config = types.ModuleType("config")
    config.app = types.SimpleNamespace(route=lambda *a, **k: (lambda f: f))
    config.freezer = None
    fake = types.ModuleType("views.schedule")
    fake.Schedule, fake.Day = Schedule, Day
    fake.__all__ = ["Schedule", "Day"]
    sys.modules.update({"flask": flask, "config": config})
    if str(OLD) not in sys.path:
        sys.path.insert(0, str(OLD))
    importlib.import_module("views")
    sys.modules["views.schedule"] = fake
    name = term_old.replace("-", "")
    module = importlib.import_module(f"views.{name}")
    return getattr(module, f"{name}schedule")()["weeks"]


# ------------------------------------------------ conversion

MONTHS = {m[:3].lower(): i for i, m in enumerate(
    "January February March April May June July August September October November December".split(), 1)}


def day_and_date(text, year):
    m = re.match(r"^\s*([A-Za-z]+)\.?\s+(\d+)", text)
    if not m or m.group(1)[:3].lower() not in MONTHS:
        return None, text.strip()
    month = MONTHS[m.group(1)[:3].lower()]
    try:
        d = datetime.date(year, month, int(m.group(2)))
    except ValueError:
        print(f"  date as written (not a real date in {year}): {text!r}")
        return None, text.strip()
    return d.strftime("%a"), d.strftime("%b ") + str(d.day)


def assignment_entry(text, link, term):
    """Return ('homework'|'project'|'note', entry)."""
    if not link:
        return "note", text
    name = link.strip("/").split("/")[-1].removesuffix(".html")
    kind = "homework" if "homework" in link else "project" if "project" in link else None
    table = HOMEWORK_USES if kind == "homework" else PROJECT_USES
    slug = table.get((term, name)) if kind else None
    if not slug:
        return "note", text
    titles = HOMEWORK if kind == "homework" else PROJECTS
    title = re.sub(r"^(Homework|Project)\s+", "", text.strip())
    title = title.replace("Project #", "#").replace("Homework #", "#")
    if re.fullmatch(r"#[\d.]+", title):
        title += f": {titles[slug][0]}"
    return kind, {"title": title, "link": f"/crypto-course/{'homework' if kind == 'homework' else 'projects'}/{slug}"}


# Semesters whose schedule page labeled each assignment "Due:" (the others
# just listed them on the day).
DUE_LABEL = {"fall2019", "fall2020", "fall2021", "winter2022", "spring2022",
             "fall2022", "winter2023", "fall2023"}


def add_due(entry, term, date):
    if term in DUE_LABEL and isinstance(entry, dict):
        entry["due"] = date
    return entry


def linked(title, link, term):
    """A slide or reading entry; links that no longer go anywhere are dropped."""
    new = new_link(link, term, 0) if link else None
    return {"title": title, "link": new} if new else {"title": title}


def convert(term_old, term):
    year = int(term[-4:])
    units = []
    for n, week in enumerate(load(term_old), 1):
        days = []
        for d in week:
            weekday, date = day_and_date(d.date, year)
            day = {"day": weekday, "date": date} if weekday else {"date": date}
            lectures = [{"title": t} for t in d.lectures if t.strip()]
            homework, projects = [], []
            for text, link in d.assignments:
                kind, entry = assignment_entry(text, link, term)
                entry = add_due(entry, term, date)
                if kind == "homework":
                    homework.append(entry)
                elif kind == "project":
                    projects.append(entry)
                elif entry.strip() and entry.strip() != "None":
                    lectures.append({"title": entry.strip()})
            if len(lectures) == 1 and re.search(r"holiday", lectures[0]["title"], re.I) and not d.slides:
                day["holiday"] = lectures[0]["title"]
            else:
                if lectures:
                    day["lectures"] = lectures
                if d.slides:
                    day["slides"] = [linked(t, l, term) for t, l in d.slides]
                if d.readings:
                    day["readings"] = [linked(t, l, term) for t, l in d.readings]
                if homework:
                    day["homework"] = homework[0] if len(homework) == 1 else homework
                if projects:
                    day["project"] = projects[0] if len(projects) == 1 else projects
            days.append(day)
        units.append({"title": f"Week {n}", "days": days})
    return {"units": units}


def write_yaml(data, path):
    import json

    def q(s):
        return json.dumps(s, ensure_ascii=False)

    lines = ["units:"]
    empty = [u["title"] for u in data["units"] if not u["days"]]
    if empty:
        print(f"  dropped weeks with no days: {', '.join(empty)}")
    for unit in (u for u in data["units"] if u["days"]):
        lines.append(f"  - title: {q(unit['title'])}")
        lines.append("    days:")
        for day in unit["days"]:
            first = True
            for key, value in day.items():
                prefix = "      - " if first else "        "
                first = False
                if isinstance(value, str):
                    lines.append(f"{prefix}{key}: {q(value)}")
                elif isinstance(value, dict):
                    lines.append(f"{prefix}{key}:")
                    lines += [f"          {k}: {q(v)}" for k, v in value.items()]
                else:
                    lines.append(f"{prefix}{key}:")
                    for item in value:
                        items = list(item.items())
                        lines.append(f"          - {items[0][0]}: {q(items[0][1])}")
                        lines += [f"            {k}: {q(v)}" for k, v in items[1:]]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    for term_old, term in TERMS:
        if term in ("winter2022", "spring2022"):
            continue  # rendered HTML only; see schedules_html.py
        data = convert(term_old, term)
        write_yaml(data, WEB / "src/data" / term / "schedule.yaml")
        days = sum(len(u["days"]) for u in data["units"])
        print(f"{term}: {len(data['units'])} weeks, {days} days")
