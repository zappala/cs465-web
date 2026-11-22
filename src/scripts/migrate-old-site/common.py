import json
import os
from pathlib import Path

OLD = Path(os.environ.get("OLD_SITE", Path.home() / "Repos/cs465/old/cs465"))
WEB = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
LINKS = HERE / "links.json"

# Old lecture folders, oldest first, and the semester that first used each.
LECTURE_DIRS = [("v1", "fall2018"), ("w19", "winter2019"), ("v2", "fall2019"),
                ("w20", "winter2020"), ("f20", "fall2020"), ("f21", "fall2021"),
                ("f22", "fall2022"), ("f23", "fall2023")]

# Old term folder names -> new semester folder names, in order.
TERMS = [("fall-2018", "fall2018"), ("winter-2019", "winter2019"), ("fall-2019", "fall2019"),
         ("winter-2020", "winter2020"), ("fall-2020", "fall2020"), ("fall-2021", "fall2021"),
         ("winter-2022", "winter2022"), ("spring-2022", "spring2022"), ("fall-2022", "fall2022"),
         ("winter-2023", "winter2023"), ("fall-2023", "fall2023")]


def load_links() -> dict:
    return json.loads(LINKS.read_text()) if LINKS.exists() else {}


def save_links(links: dict) -> None:
    LINKS.write_text(json.dumps(dict(sorted(links.items())), indent=1) + "\n")
