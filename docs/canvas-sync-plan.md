# Plan: sync assignments and the syllabus to Canvas

**Status: PROPOSED, not started.** Written 2026-11-17 with Claude, for a
future semester. Once it's built and tested, turn this file into the
documentation for using the sync (`docs/canvas-sync.md`).

## Goal

The website is the source of truth for the course. Each semester, push from
the website to Canvas:

- each assignment's **due date**, **points**, and a **description** that
  points to the assignment's page on the website;
- the **syllabus** (the full text, or a link to the website).

Today this is done by hand in Canvas, and Canvas can disagree with the site.

## What the site already has

`src/data/<semester>/schedule.yaml` lists every assignment (homework, service,
ethics, project) with a title, a link, and a due date such as `Nov 24`. Fall
2026 has 19 of them. Missing: points (each assignment's page has its rubric
total, but the YAML doesn't), the year, and the time of day.

The syllabus is `src/pages/<semester>/syllabus.mdx`, built to
`dist/<semester>/syllabus/index.html`.

## Options considered (2026-11-17)

1. **[mdxcanvas](https://github.com/BYU-CS-Course-Ops/mdxcanvas)**, written
   at BYU (v0.8.14, Nov 2026, MIT, several BYU contributors). Deploys
   assignments (due date, points, group, submission types), the syllabus,
   pages, quizzes, modules, and announcements from Markdown/XML/Jinja files,
   with a dry run.
   - For: built for BYU Canvas; colleagues use it; does far more than we need.
   - Against: Canvas content lives in its own format, a second copy of the
     course beside the Astro site (or Jinja templates that read
     `schedule.yaml`). By default its files are authoritative: items it
     tracks that are dropped from the files are deleted from Canvas. Its docs
     don't say how to take over assignments that already exist from a Canvas
     course copy (ask the authors). Pre-1.0 and changing quickly.
2. **A small sync script using [canvasapi](https://github.com/ucfopen/canvasapi)**
   (the standard Python library for the Canvas API; v3.6.0, Apr 2026). Reads
   the site's own files, so the site stays the only source. **Recommended.**
3. **A Canvas MCP server** such as
   [canvas-mcp](https://github.com/vishalsachdev/canvas-mcp) (v1.18.0, Nov
   2026, third-party). Lets Claude read and change Canvas in a conversation.
   Useful for checking that Canvas matches the site; not a repeatable sync.
   Gives a third-party program a token with all of your Canvas permissions.
4. **Canvas alone:** course copy with "adjust events and due dates" shifts
   all dates by a fixed amount. The schedule changes more than that between
   semesters.

Revisit mdxcanvas if we later want quizzes, modules, and pages managed from
files too.

## Design (option 2)

`scripts/canvas-sync.py`, run from `cs465-web`:

```sh
scripts/canvas-sync.py fall2027            # dry run: print every change
scripts/canvas-sync.py fall2027 --apply    # make the changes
scripts/canvas-sync.py fall2027 --syllabus # also replace the Canvas syllabus
```

- **Settings** in `src/data/<semester>/canvas.yaml`: Canvas URL
  (`https://byu.instructure.com`), course ID, the year, time zone
  (`America/Denver`), default due time (for example 11:59 PM), and the site
  URL for links.
- **Points:** add `points:` to each assignment in `schedule.yaml`. Check them
  against the rubric totals on the assignment pages (a test can catch
  mismatches).
- **Matching:** match each schedule assignment to a Canvas assignment by
  title; save the Canvas assignment IDs in `canvas.yaml` after the first run,
  so renaming an assignment later doesn't break the match. Report schedule
  items with no Canvas match, and Canvas assignments with no schedule item.
- **Only edit, never create or delete.** Assignments come from the Canvas
  course copy; the script updates `due_at`, `points_possible`, and the
  description.
- **Description:** a short line such as "Instructions: <link to the page on
  cs465.zappala.org>". Decide whether to replace the whole description or
  only a marked section, so anything you add by hand in Canvas survives.
- **Lists of projects** (like the v1/v2 entries in Fall 2026): both entries
  link to the same Canvas assignment; the description links both pages.
- **Syllabus:** take the main content from the built syllabus HTML and set it
  as the course's `syllabus_body` (Canvas removes the site's styling but keeps
  headings, lists, links, and tables). Or set it to a short link to the site.
  Decide which; check whether BYU or the department requires specific
  syllabus content in Canvas.
- **Locked fields:** Canvas can lock some fields (such as points and the
  description) on some assignments. Report these instead of failing.
- **Token:** a Canvas access token from your Canvas account settings, read
  from the macOS Keychain or an environment variable, never from a file in
  the repo. It has all of your Canvas permissions. (mdxcanvas documents
  personal tokens on byu.instructure.com, so BYU appears to allow them;
  confirm BYU's policy.)

## Steps

1. Decide: description style (whole or a marked section) and syllabus (full
   text or a link).
2. Add `points:` to the schedule; add a check that compares points with the
   pages' rubrics.
3. Write the script with the dry run as the default.
4. Test it against an empty sandbox course (BYU Canvas offers these) with a
   few copied assignments, then against the real course in dry-run mode.
5. Run it for real at the start of the semester and again after any schedule
   change.
6. Turn this plan into `docs/canvas-sync.md` (how to set up the token and run
   it), and add it to the semester steps in `docs/next-semester.md`.

## Open questions

- Does BYU allow personal access tokens for this (and for how long)?
- Does the department require specific syllabus content in Canvas?
- Should Canvas assignment titles also be synced from the site, or only
  dates, points, and descriptions?
- Should homework (participation-graded) and the in-class quizzes be included,
  or only projects?
