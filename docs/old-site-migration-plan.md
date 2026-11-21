# Plan: move the 2018–2023 course site into cs465-web

**Status: PLANNED 2026-11-21.** Nothing built yet.

Decided 2026-11-21: section URL `/crypto-course/`; shared pages plus small
semester pages; keep `fortune_static`; staff pages get names and roles only
(no photos or office hours); compress `Introduction-2019.pdf` (16 Keynote
slides, 10.9 MB, likely full-size photos); keep all files in git for this
migration (about 50 MB more; object storage tracked in `~/Repos/notes/TODO.md`).

The old site is `zappala/cs465` (public, Flask + Jinja + Markdown, local
copy in `~/Repos/cs465/old/cs465`). Its domain, `cs465.byu.edu`, no longer
resolves, so there are no old URLs to redirect. After the move,
`zappala/cs465` gets a README pointer and is archived.

## Goals

- Every semester from Fall 2018 to Fall 2023 browsable on
  `cs465.zappala.org`, in the same format as the current semesters (MDX
  pages, `menu.yaml`, `schedule.yaml`, `GridSchedule`).
- The front page clearly separates the 2018–2023 course from the current
  one; the organization was very different.
- One copy of each distinct page and file. The old site has 395 page files
  and 136 lecture PDFs; there are only about 45 distinct pages and 29
  distinct PDFs.
- Nothing large in git: no VM image, no big binaries, no 15 MB wordlist.

## What the old course was

The old front page described three parts: **cryptography** (symmetric and
public key primitives, MACs, hash functions), **systems** that use
cryptography (HTTPS/TLS, PKI, secure email, Signal), and **software
security** (buffer overflows, integer bugs), plus passwords and social
engineering. Projects 1 to 6 and 10, and most homework, are cryptography.
So it is mostly, but not only, an applied cryptography course: roughly the
first two thirds of the semester, with software security and human
factors at the end. The current course (2024 on) is a broad introduction
organized around OS security, software security, Rust and cryptography,
web security, and threat modeling.

Suggested front page label: **"2018–2023: cryptography-focused course"**
(alternatives: "Applied Cryptography and Security", "Cryptography,
Systems, and Software Security", the old site's own three parts).

| Semester | Instructor | Notes |
| --- | --- | --- |
| Fall 2018 | Daniel Zappala | |
| Winter 2019 | Fred Clift | |
| Fall 2019 | Daniel Zappala | |
| Winter 2020 | Fred Clift | |
| Fall 2020 | Fred Clift | |
| Fall 2021 | Fred Clift | |
| Winter 2022 | Brett Decker | Saved as rendered HTML, no schedule source |
| Spring 2022 | Tarun Kumar Yadav | Saved as rendered HTML, no schedule source |
| Fall 2022 | Fred Clift | |
| Winter 2023 | James Conners | Study guides are "TBD" |
| Fall 2023 | Fred Clift | Last semester of this course |

## Inventory of the old site

| Kind | Files | Distinct | Notes |
| --- | ---: | ---: | --- |
| Projects | 11 × 11 + extras | 19 | Includes 3 Fall 2023 rewrites and 3 tutorials |
| Homework | about 170 | 21 | Numbers moved between semesters (see the table below) |
| Study guides | 22 | 3 | Plus Winter 2023 "TBD" placeholders |
| Syllabus (`index.html`) | 11 | 3 | Fall 2018 style, Fall 2019 style, Fall 2023 |
| Staff (`help/instructor`, `officehours`, `slack`) | 30 | about 25 | All semester-specific |
| Schedules | 9 Python files in `views/`, 2 rendered pages | 11 | |
| Lectures pages | 9 | 1 | Each just lists the PDF folder |
| Lecture PDFs | 136 (210 MB) | 29 (48.7 MB) | `static/lectures/<term>/` |
| Readings (`static/pubs`) | 4 (0.9 MB) | 4 | FIPS 197, FIPS 180-3, two HMAC papers |
| Handout files (`static/files`) | 14 (18 MB) | 14 | 15.6 MB is `cracklib.txt` |
| Images (`static/img`) | 17 (10 MB) | 17 | 9.7 MB is VM setup screenshots |
| Not content | | | `menu.html`, `base.html`, `save.html` (a test page), `misc.html` (one link), `404.html` |

## Where things go

### URLs and folders

Two kinds of content:

1. **Shared pages**, one copy each, under a new section
   **`/crypto-course/`** (name to confirm; it must not start with a
   semester name):

   ```text
   src/pages/crypto-course/
     index.mdx                 overview: the course, semesters, links to everything
     syllabus-2018.mdx         syllabus versions (3)
     syllabus-2019.mdx
     syllabus-2023.mdx
     lectures.mdx              all 29 slide decks, with the semesters that used each
     projects/*.mdx            19 pages
     homework/*.mdx            21 pages
     study-guides/*.mdx        3 pages
   src/data/crypto-course/menu.yaml
   ```

   Each shared page starts with a small `UsedIn` notice: "Used in Fall 2018
   to Fall 2023 (as Project 1)", with semester links. Small differences
   between semesters go in an "Earlier versions" section at the bottom
   (as in the archived project repos' `history.md`).

2. **Per-semester pages**, small, under `/fall2018`, `/winter2019`, ...
   `/fall2023`, `/winter2022`, `/spring2022`, `/winter2023` (no clash with
   the current `fall2024`+ folders):

   ```text
   src/pages/fall2023/index.mdx      the schedule (GridSchedule), like current semesters
   src/pages/fall2023/staff.mdx      instructor, TAs, office hours, Slack
   src/data/fall2023/menu.yaml       Home, Syllabus, Staff, Projects, Homework, Lectures, Study guides
   src/data/fall2023/schedule.yaml   converted from views/fall2023.py
   ```

   The semester menu's Syllabus, Projects, Homework, Lectures and Study
   guides entries link to the shared pages, with each semester's own
   numbering ("Project 8: Extracting Secrets" in Fall 2020, "Project 9" in
   Fall 2018).

Result: about 45 shared MDX pages plus 22 small semester pages and 22
YAML files, instead of 395 page files.

**Alternative (not recommended):** one dynamic route
`src/pages/[semester]/[...slug].astro` that renders shared content under
every semester's URL with that semester's menu. Per-semester URLs and
menus everywhere, still one source file per version, but more machinery
than the rest of the site uses.

### Code changes needed

- **Links outside the semester prefix.** `Dropdown.jsx`, `MenuBar` and
  `GridSchedule.jsx` always build `prefix + url`. Add one rule: a URL that
  starts with `/crypto-course/` (or any URL with an explicit
  `absolute: true`) is used as is. Check every current menu and schedule
  still renders the same (build output diff).
- **Math.** Old pages use MathJax (`$...$`, `$$...$$`), mainly Projects 4
  and 5, Homework 7, and a study guide. Add `remark-math` + `rehype-katex`
  (and the KaTeX CSS) to `astro.config.mjs`. Check that `$` in shell
  examples on other pages doesn't turn into math (escape as `\$`).
- **`UsedIn` component** (like `VersionNotice`), and a `crypto-course`
  menu.
- `Semester.astro` defaults the semester to `fall2024` when it can't tell;
  shared pages need `/crypto-course` to load their own menu (they will,
  since the first path segment is `crypto-course`).

### Front page (`src/pages/index.mdx`)

```text
## Current Semester            (unchanged)
## Course Description          (unchanged; the current course)
## Past semesters              Winter 2026 ... Winter 2024 (unchanged)

## 2018–2023: cryptography-focused course
A short paragraph: the three parts (cryptography, systems that use it,
software security), that projects were mostly implementing cryptography
(AES, hash and MAC attacks, Diffie-Hellman, RSA), and that the course was
reorganized in 2024. Link: "All projects, homework and slides" →
/crypto-course. Then the 11 semesters with instructors, newest first.
```

Use a visible separator (a heading plus a light box, or a `Card`) so the
two courses don't read as one list.

### Projects

Slug in `src/pages/crypto-course/projects/`. "All" means all 11 semesters.

| Slug | Title | Semesters (number) | Notes |
| --- | --- | --- | --- |
| `aes` | AES | All (1) | Differences: grader link; Fall 2018–Winter 2020 printed Appendix C instead |
| `hash-attack` | Hash Attack | All (2) | Report length 1–2 → 2–4 pages in Winter 2019/2020 |
| `mac-attack` | MAC Attack | All (3) | Three different published MACs; list them in Earlier versions |
| `diffie-hellman` | Diffie-Hellman | All (4) | Math; the server's naming table until Fall 2020 |
| `rsa` | RSA | All (5) | Math |
| `tls` | TLS | All (6) | Small wording changes over time |
| `password-cracking` | Password Cracking | Fall 2018–Winter 2023 (7) | Links `passwd.txt`, `shadow.txt`, wordlist |
| `password-cracking-2023` | Password Cracking (VM version) | Fall 2023 (7) | Plus the John/hashcat tutorial |
| `buffer-overflow` | Buffer Overflow | Fall 2018–Winter 2020 (8), Fall 2020–Winter 2023 (9) | `sample3.tar` |
| `buffer-overflow-2023` | Buffer Overflow (VM version) | Fall 2023 (9) | `overflow.c`, `overflow2.c`, `overflow`, `shell_test.c` |
| `extracting-secrets` | Extracting Secrets | Fall 2018–Winter 2020 (9), Fall 2020–Winter 2023 (8) | `fortune_static`, `fortunes.enc` (see Files) |
| `extracting-secrets-2023` | Extracting Secrets (VM version) | Fall 2023 (8) | `secret_treasure`, `treasures.enc` |
| `smime-pgp` | S/MIME and PGP | All (10) | |
| `bomb` | Bomb (extra credit) | Fall 2018–Fall 2019 (11); kept unlisted as `project11.old` later | |
| `ringzer0` | RingZer0 (extra credit) | Winter 2020–Fall 2023 (11) | |
| `virtual-machine-setup` | Virtual machine setup | Fall 2023 | VM image link is on a department page (`~cs465ta/cs465vm.ova`); note it may be gone |
| `gdb-tutorial` | gdb tutorial | Fall 2023 | |
| `john-hashcat-tutorial` | John the Ripper and hashcat | Fall 2023 | By a TA; `misc.html` just linked it |

Grader links (`grader.cs465.byu.edu`, `cs465.byu.edu/projectN-autograder`,
`sebulba.cs.byu.edu`) become plain text with a note that the graders were
retired. Don't link the private project repos from this public site.

### Homework

Slug in `src/pages/crypto-course/homework/`. Numbers in parentheses are
the homework numbers in those semesters. Notably, Fall 2020/2021 shifted
Homework 8–12 down by one, and the 95–98 numbers were unlisted extras.

| Slug | Topic | Semesters (number) |
| --- | --- | --- |
| `about-you` | Background survey | Fall 2020 (0) |
| `news` | Security news story | All (1) |
| `finite-field-arithmetic` | Finite field pseudocode | All (2) |
| `block-cipher-modes` | Block cipher modes | All (3) |
| `mac-attack-prep` | Preparing for the MAC attack | All (4) |
| `diffie-hellman` | Diffie-Hellman and man in the middle | All (5) |
| `aes-library` | Using an AES library | Fall 2018/2019 (6); later as 97 |
| `mac-then-encrypt` | MAC-then-encrypt vs. encrypt-then-MAC | Winter 2019–Fall 2023 (6) |
| `rsa-keys` | RSA keys by hand | All (7) |
| `tls-intro` | "First few milliseconds of HTTPS" summary | Fall 2021 (7.5), Winter 2022–Fall 2023 (8) |
| `tls-attacks` | TLS attacks | Fall 2018–Winter 2020 (8); later as 95 |
| `password-research` | Administrator's guide to password research | All (9; 8 in Fall 2020/2021) |
| `gdb-intro` | Introduction to gdb | Fall 2018–Winter 2023 (10; 9 in Fall 2020/2021) |
| `gdb-stack-frames` | gdb, stack frames and registers (rewrite) | Fall 2023 (10) |
| `buffer-overflow-history` | Recent or historic buffer overflows | Fall 2018/2019 (11); later as 96 |
| `smashing-the-stack` | Three papers on stack smashing | Winter 2019–Fall 2023 (11; 10 in Fall 2020/2021) |
| `privacy-vs-public-good` | Individual privacy vs. the public good | Fall 2022–Fall 2023 (11.5) |
| `trusting-trust` | Reflections on Trusting Trust | All (12; 11 in Fall 2020/2021) |
| `social-engineering` | Social engineering (extra credit) | Winter 2019–Fall 2021 (13, 98), Fall 2020–Fall 2023 (12/13); 2 versions, check |
| `penetration-testing` | Penetration testing (extra credit) | Winter 2023 (13) |

### Study guides, syllabus, staff, lectures

| Old | New |
| --- | --- |
| `help/study-guide-midterm1` (2 versions) | `crypto-course/study-guides/midterm-1-2018.mdx` (Fall 2018/2019, a real guide) and `midterm-1.mdx` (later semesters: mostly exam logistics) |
| `help/study-guide-midterm2` (1 version) | `crypto-course/study-guides/midterm-2.mdx` |
| Winter 2023 "TBD" study guides | Not copied; Winter 2023's menu omits them |
| `index.html` (syllabus, 3 versions) | `crypto-course/syllabus-2018.mdx`, `-2019.mdx`, `-2023.mdx`; semester-specific lines (times, rooms) listed at the top of each |
| `help/instructor`, `help/officehours`, `help/slack` | Merged into each semester's `staff.mdx` |
| `lectures.html` (per semester) | One `crypto-course/lectures.mdx` |
| `views/<term>.py` schedules | `src/data/<term>/schedule.yaml`: one unit per week ("Week 1", ...), lecture topics as lectures without links, slides, readings, and homework/project entries pointing to the shared pages. "No class" and holidays use `holiday`; exams use `exam` |
| Winter/Spring 2022 rendered `schedule` | Same, parsed from the HTML table |

### Files

All under `public/`, organized like the current site.

| What | Old | New | Size in git |
| --- | --- | --- | --- |
| Lecture PDFs, 23 names with one version | `static/lectures/<term>/X.pdf` (up to 7 copies) | `public/lectures/crypto-course/X.pdf` | |
| 6 names with several versions | `Introduction`, `Terminology`, `Cryptography`, `Diffie-Hellman`, `RSA`, `MAC` | `X-2018.pdf` (`v1`), `X-2019.pdf` (`w19`/`w20`), `X-2020.pdf` (`f20`–`f23`); `MAC-2019.pdf` for `v2` | 48.7 MB total, about 38 MB after compressing `Introduction-2019.pdf` (decided); check the slides still look right |
| Readings | `static/pubs/*.pdf` | `public/lectures/crypto-course/readings/` | 0.9 MB |
| Small handouts | `passwd.txt`, `shadow.txt`, `plaintext.txt`, `dh.zip`, `overflow*.c`, `overflow`, `shell_test.c`, `sample3.tar`, `secret_treasure`, `treasures.enc`, `fortunes.enc` | `public/code/crypto-course/<project>/` | about 0.4 MB |
| `cracklib.txt` (15.6 MB) | | **Not copied.** Link to the upstream cracklib wordlist instead | 0 |
| `fortune_static` (1.7 MB binary) | `static/files/secrets/` | `public/code/crypto-course/extracting-secrets/` (decided: keep) | 1.7 MB |
| VM screenshots (9.7 MB PNG) | `static/img/vm/` | `src/images/crypto-course/vm/`, converted to WebP or resized | about 1 MB |
| Diagrams | `tasched.png`, `func1.png`, `func2.png` | `src/images/crypto-course/` | 0.2 MB |
| Staff photos | `FredClift.jpg`, `daniel-zappala.jpg`, `james-conners.jpg`, `tarun_photo.jpg` (Brett Decker's and Travis Feller's are missing) | Not copied (decided: names and roles only) | 0 |
| VM image | Linked only (`~cs465ta/cs465vm.ova`) | Link kept, with a note | 0 |

Expected growth of the repo: about 40 MB (currently 142 MB of git history,
with 55 MB of code and 25 MB of lectures in `public/`).

## How to convert

One-time scripts in `src/scripts/migrate-old-site/` (deleted after the
move, or kept in the archived old repo):

1. **Schedules:** import each `views/<term>.py` with a stub `Schedule`
   class that records `week`, `day`, `lecture`, `slide`, `reading`,
   `assignment` calls, then write `schedule.yaml`. Map old links with the
   table below. Parse the two rendered 2022 schedules from HTML.
2. **Pages:** take the Markdown inside `{% filter markdown %}`, drop the
   Jinja tags, and turn it into MDX: escape `{`, `}` and stray `<`, fix
   HTML attributes for JSX (`class` → `className`), make math work, and
   rewrite links. For each shared page, start from the newest version and
   write the "Earlier versions" notes by hand from a diff of the others.
   The rendered 2022 pages are only needed for their schedules and staff
   pages; their projects and homework match other semesters.
3. **Files:** copy only the deduplicated set (hash-checked), with the new
   names.

Link rewriting:

| Old | New |
| --- | --- |
| `/<term>/projects/projectN` | `/crypto-course/projects/<slug>` for that term's numbering |
| `/<term>/homework/homeworkN` | `/crypto-course/homework/<slug>` for that term's numbering |
| `/<term>/help/study-guide-*` | `/crypto-course/study-guides/...` |
| `/<term>/help/instructor`, `officehours`, `slack` | `/<newterm>/staff` |
| `/<term>/projects/gdb_tutorial` etc. | `/crypto-course/projects/gdb-tutorial` etc. |
| `/static/lectures/<dir>/X.pdf` | `/lectures/crypto-course/X[-year].pdf` by hash |
| `/static/pubs/X.pdf` | `/lectures/crypto-course/readings/X.pdf` |
| `/static/files/...` | `/code/crypto-course/<project>/...` |
| `grader.cs465.byu.edu`, `sebulba.cs.byu.edu`, `cs465.byu.edu/...autograder` | Plain text plus "(retired)" |
| Learning Suite, Piazza, Slack mentions | Left as written (historical) |

## Order of work (one commit per step, on a branch, draft PR for a Netlify preview)

1. Code changes: absolute links in menus and schedules, math, `UsedIn`,
   `crypto-course` menu. Verify the current semesters' built output is
   unchanged.
2. Files: lectures, readings, handouts, images.
3. Shared pages: projects, then homework, study guides, syllabus versions,
   lectures page, `crypto-course/index.mdx`.
4. Semesters, oldest first: `schedule.yaml`, `menu.yaml`, `index.mdx`,
   `staff.mdx`.
5. Front page section.
6. Verify (below), then merge.
7. Old repo: README pointer to `cs465.zappala.org/crypto-course`, archive
   `zappala/cs465` on GitHub. Then delete `~/Repos/cs465/old/` after
   checking nothing else is needed from it.

## Verification

- Build passes; every internal link and file link resolves (add a
  post-build link check if there isn't one).
- **Nothing lost:** a script lists every old page and every old link and
  shows where each landed (shared page, semester page, or deliberately
  dropped).
- **Text check:** for each shared page, the newest old version's text
  matches the new page's text apart from the notes added; for each
  semester, every schedule day and item is present.
- Math renders on the DH, RSA and Homework 7 pages; `$` in shell examples
  doesn't.
- Phone widths (320–768 px) on a schedule, a project, and the front page:
  no horizontal scroll (wide tables and code blocks are the risk).
- Current semesters' pages render exactly as before (diff the built HTML
  text).

## Decisions (all made 2026-11-21)

1. Section name and URL: `/crypto-course/`, label "2018–2023:
   cryptography-focused course".
2. Shared pages plus small semester pages (not the dynamic route).
3. `Introduction-2019.pdf`: compress it.
4. `fortune_static`: keep.
5. Staff pages: names and roles only; no photos, no office hour times.
6. Large files: keep in git for this migration. Whether to move
   `cs465-web` files to R2 is a separate to-do in `~/Repos/notes/TODO.md`.
