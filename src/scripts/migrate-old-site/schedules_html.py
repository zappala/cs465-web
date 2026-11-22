"""Winter 2022 and Spring 2022 only survive as rendered pages: parse their
schedule HTML into schedule.yaml."""

import html
import re

from common import OLD, WEB
from convert import new_link
from schedules import add_due, assignment_entry, day_and_date, write_yaml


def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def links(fragment):
    return [(text(t), h) for h, t in re.findall(r'<a href="([^"]*)"[^>]*>(.*?)</a>', fragment, re.S)]


def convert(term_old, term):
    page = (OLD / "templates" / term_old / "schedule").read_text()
    page = page[page.find('id="page"'):]
    year = int(term[-4:])
    units = []
    for week in re.split(r'<h2 class="plain">', page)[1:]:
        title = text(week.split("</h2>")[0])
        days = []
        for block in re.findall(r'<div class="schedule">(.*?)\n</div>', week, re.S):
            date_text = text(re.search(r'<div class="day">(.*?)</div>', block, re.S).group(1))
            weekday, date = day_and_date(date_text, year)
            day = {"day": weekday, "date": date} if weekday else {"date": date}
            cols = re.split(r'<span class="section">Assignments</span>', block)
            first, second = cols[0], cols[1] if len(cols) > 1 else ""
            lectures = [{"title": text(s)} for s in re.findall(r'<span class="section">(.*?)</span>', first, re.S)
                        if text(s)]
            slides, readings = [], []
            for li in re.findall(r"<li>(.*?)</li>", first, re.S):
                label = text(li)
                target = slides if label.startswith("Slides:") else readings
                found = links(li)
                if found:
                    t, h = found[0]
                    target.append({"title": t, "link": new_link(h, term, 0)})
                else:
                    target.append({"title": re.sub(r"^(Slides|Reading):\s*", "", label)})
            homework, projects = [], []
            for item in re.findall(r'<span class="due">(.*?)</span>', second, re.S):
                found = links(item)
                t, h = found[0] if found else (re.sub(r"^Due:\s*", "", text(item)), None)
                kind, entry = assignment_entry(t, h, term)
                entry = add_due(entry, term, date)
                if kind == "homework":
                    homework.append(entry)
                elif kind == "project":
                    projects.append(entry)
                elif entry and entry != "None":
                    lectures.append({"title": entry})
            if lectures: day["lectures"] = lectures
            if slides: day["slides"] = slides
            if readings: day["readings"] = readings
            if homework: day["homework"] = homework[0] if len(homework) == 1 else homework
            if projects: day["project"] = projects[0] if len(projects) == 1 else projects
            days.append(day)
        units.append({"title": title, "days": days})
    return {"units": units}


if __name__ == "__main__":
    for term_old, term in (("winter-2022", "winter2022"), ("spring-2022", "spring2022")):
        data = convert(term_old, term)
        write_yaml(data, WEB / "src/data" / term / "schedule.yaml")
        print(f"{term}: {len(data['units'])} weeks, {sum(len(u['days']) for u in data['units'])} days")
