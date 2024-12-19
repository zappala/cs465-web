# CS 465 Website

## 🧞 Commands

This project uses the [astro](https://astro.build) framework. All commands are
run from the root of the project, from a terminal:

| Command                   | Action                                           |
| :------------------------ | :----------------------------------------------- |
| `npm install`             | Installs dependencies                            |
| `npm run dev`             | Starts local dev server at `localhost:4321`      |
| `npm run build`           | Build your production site to `./dist/`          |
| `npm run preview`         | Preview your build locally, before deploying     |
| `npm run astro ...`       | Run CLI commands like `astro add`, `astro check` |
| `npm run astro -- --help` | Get help using the Astro CLI                     |

Commits to the main branch will be automatically built at netlify and deployed
to `cs465.zappala.org`.

## Website Structure

```text
/
├── public/
│   └── favicon.svg
│   ├── code/
│   ├── images/
│   ├── lectures/
├── src/
│   ├── components/*.jsx
│   ├── data/
│   ├── images/
│   ├── layouts/
│   ├── menu/*.jsx
│   └── pages/
│   ├── scripts/
└── package.json
```

- public
  - code: starter code for projects, organized into subfolders as
    `name/version/files`
  - images: used only for instructor and TA images
  - lectures: lecture PDFs, organized into subfolders as `semester/files`
- src
  - components: React components for the site
  - data: menu and weekly schedule, organized into subfolders as
    `semester/*.yaml`
  - images: images used in homework, projects, notes
  - layouts: templates for pages
  - menu: components for the menu
  - pages: extended markdown (mdx) that can mix React components and Markdown,
    organized as `semester`
  - scripts: maintenance scripts

## Starting a new semester

All content is in MDX files and all organization (menus, schedule) is in YAML
files.

1. run `npm run dev`
1. make a copy of `pages/PREVIOUS_SEMESTER` into `pages/CURRENT_SEMESTER`
1. make a copy of `data/PREVIOUS_SEMESTER` into `data/CURRENT_SEMESTER`
1. edit `src/pages/index.mdx` to list the previous semester and highlight the
   current semester
1. edit `src/pages/SEMESTER/index.mdx` to include the prefix for the current
   semester
1. edit `src/data/SEMESTER/menu.yaml` to name the current semester and adjust
   the menu if desired
1. edit `src/data/SEMESTER/schedule.yaml` to adjust the weekly schedule for the
   current semester
1. edit `src/pages/SEMESTER/staff.mdx` to modify the staff for this semester
1. edit `src/pages/SEMESTER/syllabus.mdx` to modify the syllabus for this
   semester
1. edit any other content as you desire, e.g. notes, homework, projects

## Astro help

See [the documentation](https://docs.astro.build) or jump into the
[Discord server](https://astro.build/chat).
