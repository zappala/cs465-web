"""'Earlier versions' notes for the shared pages, written from a diff of
every semester's copy against the newest one. Markdown, appended to the page.
Pass-off site links are listed per page; the graders are retired."""

PASSOFF = {
    "sebulba": "a PHP page on `sebulba.cs.byu.edu`",
    "2020": "`cs465.byu.edu`",
    "2021": "`grader.cs465.byu.edu`",
}

NOTES = {
    "aes": f"""
- Fall 2018 to Winter 2020 had no grader. Instead: "When we run your code,
  it should, without any input from the command line or command line
  options, print out all of the test cases in Appendix C of the FIPS
  specification, with the debug information for each round." Fall 2018
  and Fall 2019 linked the [older AES slides](/lectures/crypto-course/AES-fall2018.pdf).
- Fall 2020 passed off on {PASSOFF['2020']}; Fall 2021 to Fall 2023 on
  {PASSOFF['2021']}, with a screenshot of the result in the submission.
""",
    "hash-attack": """
- Fall 2018 and Fall 2019: a 1 to 2 page report (2 to 4 from Winter 2019
  on); example sizes "8, 16, 20, 24" (10 added later); no requirement for
  non-multiple-of-8 sizes; "number of attempts" without "(hashes)"; no
  stated target audience.
- Winter 2019 also lacked "think: reproducibility" in the rubric and
  "(mildly)" in "may (mildly) differ".
""",
    "mac-attack": f"""
The message was always the same, but the published MAC (and so the
grader's key) changed:

| Semesters | MAC | Pass-off |
| --- | --- | --- |
| Fall 2018 to Fall 2019 | `f4b645e89faaec2ff8e443c595009c16dbdfba4b` | {PASSOFF['sebulba']} |
| Winter 2020 | `3875cb851ed7e35a916ee4a9685117c38129eda0` | `167.172.158.71/lab3/` |
| Fall 2020 | `3875cb…` | {PASSOFF['2020']} |
| Fall 2021 to Winter 2023 | `3875cb…` | {PASSOFF['2021']} |
| Fall 2023 | `e384efadf26767a613162142b5ef0efbb9d7659a` | {PASSOFF['2021']} |

Fall 2018 to Fall 2019 also showed the MAC with spaces between bytes, and
Fall 2018 and Fall 2019 told students to ignore the pass-off site's
"email the TAs" message and contact the instructor on Piazza instead.
""",
    "diffie-hellman": f"""
- Pass-off: {PASSOFF['sebulba']} (Fall 2018 to Fall 2019), `cs465.byu.edu/lab4/`
  (Winter 2020), {PASSOFF['2020']} (Fall 2020), {PASSOFF['2021']} (Fall 2021
  on).
- Up to Fall 2020 the page had a table: "the pass-off server names the
  values differently": it called $g^b \\bmod p$ "$g^t \\bmod p$" (line 1 of
  its output), $b$ "T" (line 2), and $g^{{ab}}$ "${{g^t \\bmod p}}^s \\bmod p$"
  (line 3).
- Fall 2018 to Winter 2020 wrote the identity as $(g^a)^b = (g^b)^a = g^{{ab}} = g^{{ba}}$.
""",
    "rsa": f"""
- Only the pass-off site changed: {PASSOFF['sebulba']} (Fall 2018 to Fall
  2019), `cs465.byu.edu/lab5/` (Winter 2020), {PASSOFF['2020']} (Fall
  2020), {PASSOFF['2021']} (Fall 2021 on).
""",
    "tls": """
- Fall 2018 and Fall 2019 didn't mention testssl.sh, didn't ask students
  to explain the cryptographic guarantees of at least 3 samples, and had no
  bonus for non-HTTP TLS services.
""",
    "buffer-overflow": """
- Fall 2018 to Winter 2020 used the smaller Ubuntu 16.04 VM (Fall 2020 on:
  the Ubuntu 18 VM, with login details).
- Fall 2018 and Fall 2019 had no note on compiler flags for recompiling and
  didn't ask students to vary the input length (to at least 35
  characters).
- Fall 2018 to Winter 2020 lacked the clarification: use the debugger to
  estimate where the return address goes, then exploit from the command
  line without it.
""",
    "extracting-secrets": """
- Fall 2018 and Fall 2019 lacked the note that probabilistic methods of
  extracting all the fortunes won't receive full credit.
""",
    "ringzer0": """
- Winter 2020: extra credit for up to 40 RingZer0 points, at two class
  points per RingZer0 point (later: up to 25, with the 50-point cap stated).
- Winter 2020 to Winter 2023: 3 extra points (not 2) for reporting your
  "(not that great)" ranking, and a "1% bump" (not "half a letter grade,
  e.g. +5% overall") for the last item.
""",
    "news": """
- The due dates were each semester's months (e.g. Jan/Feb/Mar in winter).
- Fall 2018 and Fall 2019 posted stories on Piazza; Winter 2019 and Winter
  2020 linked a Slack invitation.
""",
    "finite-field-arithmetic": """
- Fall 2018 to Winter 2020 didn't ask for the `xtime` pseudocode.
""",
    "block-cipher-modes": """
- Fall 2018: hand in a printout in class. Fall 2019: a PDF in Learning
  Suite.
""",
    "mac-then-encrypt": """
- Winter 2019 and Winter 2020 had no alternate link for the reading.
""",
    "tls-intro": """
- Winter 2022 and Spring 2022 didn't add "so we can move briskly through
  the material in class."
""",
    "gdb-intro": """
- Fall 2018 to Winter 2020 didn't have the two example images.
""",
    "smashing-the-stack": """
- Before Fall 2023, the third paper was "Smashing the Stack for Fun and
  Profit Today", not "Smashing the stack in the 21st century".
""",
}
