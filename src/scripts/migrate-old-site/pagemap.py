"""Which old page, in which semester, became which shared page.

Built from a text-similarity clustering of every semester's pages
(numbers moved between semesters). Terms use the new names (fall2018...).
"""

ALL = ["fall2018", "winter2019", "fall2019", "winter2020", "fall2020", "fall2021",
       "winter2022", "spring2022", "fall2022", "winter2023", "fall2023"]
NAMES = {t: t[:-4].capitalize() + " " + t[-4:] for t in ALL}  # fall2018 -> "Fall 2018"


def terms(spec):
    """'all', 'fall2018-winter2020', or 'fall2018,fall2019' -> list of terms."""
    if spec == "all":
        return list(ALL)
    out = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            out += ALL[ALL.index(a): ALL.index(b) + 1]
        else:
            out.append(part)
    return out


# slug: (title, [(terms, old file name, number shown to students or None if unlisted)])
PROJECTS = {
    "aes": ("AES", [("all", "project1", "1")]),
    "hash-attack": ("Hash Attack", [("all", "project2", "2")]),
    "mac-attack": ("MAC Attack", [("all", "project3", "3")]),
    "diffie-hellman": ("Diffie-Hellman", [("all", "project4", "4")]),
    "rsa": ("RSA", [("all", "project5", "5")]),
    "tls": ("TLS", [("all", "project6", "6")]),
    "password-cracking": ("Password Cracking", [("fall2018-winter2023", "project7", "7")]),
    "password-cracking-2023": ("Password Cracking (VM version)", [("fall2023", "project7", "7")]),
    "buffer-overflow": ("Buffer Overflow", [("fall2018-winter2020", "project8", "8"),
                                            ("fall2020-winter2023", "project9", "9")]),
    "buffer-overflow-2023": ("Buffer Overflow (VM version)", [("fall2023", "project9", "9")]),
    "extracting-secrets": ("Extracting Secrets", [("fall2018-winter2020", "project9", "9"),
                                                  ("fall2020-winter2023", "project8", "8")]),
    "extracting-secrets-2023": ("Extracting Secrets (VM version)", [("fall2023", "project8", "8")]),
    "smime-pgp": ("S/MIME and PGP", [("all", "project10", "10")]),
    "bomb": ("Bomb (Extra Credit)", [("fall2018-fall2019", "project11", "11"),
                                     ("winter2020,fall2020,fall2021,fall2022,winter2023,fall2023",
                                      "project11.old", None)]),
    "ringzer0": ("RingZer0 (Extra Credit)", [("winter2020-fall2023", "project11", "11")]),
    "virtual-machine-setup": ("Virtual Machine Setup", [("fall2023", "virtual_machine_setup", None)]),
    "gdb-tutorial": ("gdb Tutorial", [("fall2023", "gdb_tutorial", None)]),
    "john-hashcat-tutorial": ("Cracking Passwords with John the Ripper and hashcat",
                              [("fall2023", "jtr_hashcat_tutorial", None)]),
}

HOMEWORK = {
    "about-you": ("About You", [("fall2020", "homework0", "0")]),
    "news": ("Security News", [("all", "homework1", "1")]),
    "finite-field-arithmetic": ("Finite Field Arithmetic", [("all", "homework2", "2")]),
    "block-cipher-modes": ("Block Cipher Modes", [("all", "homework3", "3")]),
    "mac-attack-prep": ("Preparing for the MAC Attack", [("all", "homework4", "4")]),
    "diffie-hellman": ("Diffie-Hellman", [("all", "homework5", "5")]),
    "aes-library": ("Using an AES Library", [("fall2018,fall2019", "homework6", "6"),
                                            ("winter2019,winter2020,fall2020,fall2021,fall2022,winter2023,fall2023",
                                             "homework97", None)]),
    "mac-then-encrypt": ("MAC-then-Encrypt or Encrypt-then-MAC",
                         [("winter2019,winter2020,fall2020,fall2021,winter2022,spring2022,fall2022,winter2023,fall2023",
                           "homework6", "6")]),
    "rsa-keys": ("Generating RSA Keys", [("all", "homework7", "7")]),
    "tls-intro": ("TLS Introduction", [("fall2021", "homework7.5", "7.5"),
                                       ("winter2022,spring2022,fall2022,winter2023,fall2023", "homework8", "8")]),
    "tls-attacks": ("TLS Attacks", [("fall2018-winter2020", "homework8", "8"),
                                    ("fall2020,fall2021,fall2022,winter2023,fall2023", "homework95", None)]),
    "password-research": ("Internet Password Research",
                          [("fall2018-winter2020,winter2022,spring2022,fall2022,winter2023,fall2023", "homework9", "9"),
                           ("fall2020,fall2021", "homework8", "8")]),
    "gdb-intro": ("Introduction to gdb", [("fall2018-winter2020,winter2022,spring2022,fall2022,winter2023", "homework10", "10"),
                                          ("fall2020,fall2021", "homework9", "9")]),
    "gdb-stack-frames": ("gdb, Stack Frames, and Registers", [("fall2023", "homework10", "10")]),
    "buffer-overflow-history": ("Buffer Overflows in the Wild",
                                [("fall2018,fall2019", "homework11", "11"),
                                 ("winter2019,winter2020,fall2020,fall2021,fall2022,winter2023,fall2023", "homework96", None)]),
    "smashing-the-stack": ("Smashing the Stack",
                           [("winter2019,winter2020,winter2022,spring2022,fall2022,winter2023,fall2023", "homework11", "11"),
                            ("fall2020,fall2021", "homework10", "10")]),
    "privacy-vs-public-good": ("Individual Privacy vs. Greater Public Good",
                               [("fall2022,winter2023,fall2023", "homework11.5", "11.5")]),
    "trusting-trust": ("Reflections on Trusting Trust",
                       [("fall2018-winter2020,winter2022,spring2022,fall2022,winter2023,fall2023", "homework12", "12"),
                        ("fall2020,fall2021", "homework11", "11")]),
    "social-engineering": ("Social Engineering (Extra Credit)",
                           [("winter2019,winter2020", "homework13", "13"),
                            ("winter2019,winter2020,fall2020,fall2021", "homework98", None),
                            ("fall2020,fall2021", "homework12", "12"),
                            ("winter2022,spring2022,fall2022,fall2023", "homework13", "13")]),
    "penetration-testing": ("Penetration Testing (Extra Credit)", [("winter2023", "homework13", "13")]),
}


def uses(table):
    """(term, old file) -> slug, for link rewriting."""
    out = {}
    for slug, (_, rows) in table.items():
        for spec, old, _number in rows:
            for t in terms(spec):
                out[(t, old)] = slug
    return out
