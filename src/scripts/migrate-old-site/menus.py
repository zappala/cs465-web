"""Write src/data/crypto-course/menu.yaml for the shared pages."""

from common import WEB
from pagemap import HOMEWORK, PROJECTS


def quote(s):
    return '"' + s.replace('"', '\\"') + '"'


def crypto_course_menu():
    lines = ["menu:", "  semester: 2018–2023 Course", "  items:",
             "    - title: Overview", "      url: /",
             "    - title: Projects", "      submenu:"]
    for slug, (title, _) in PROJECTS.items():
        lines += [f"        - title: {quote(title)}", f"          url: projects/{slug}"]
    lines += ["    - title: Homework", "      submenu:"]
    for slug, (title, _) in HOMEWORK.items():
        lines += [f"        - title: {quote(title)}", f"          url: homework/{slug}"]
    lines += ["    - title: Exams", "      submenu:",
              "        - title: Midterm 1 (2018-2019)", "          url: study-guides/midterm-1-2018",
              "        - title: Midterm 1", "          url: study-guides/midterm-1",
              "        - title: Midterm 2", "          url: study-guides/midterm-2",
              "    - title: Lectures", "      url: /lectures"]
    path = WEB / "src/data/crypto-course/menu.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    crypto_course_menu()
