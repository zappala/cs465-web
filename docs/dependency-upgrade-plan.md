# Plan: upgrade the site's dependencies (Astro 7, Tailwind 4, React 19)

**Status: PLANNED 2026-11-21** (revised the same day: math to MathML and
Astro 7's default Markdown processor). Not started. Replaces the "Upgrade the site's
dependencies" item in [next-semester.md](next-semester.md).

## Goal

Move to current major versions with **no visible change** to any page: same
text, same links, same look on desktop and phone. Every step is checked
against a saved build of today's site.

| Package | Now | Target | Notes |
| --- | --- | --- | --- |
| `astro` | 5.18 | 7.4 | through 6; Node 22.23.4 or newer |
| `@astrojs/mdx` | 4.3 | 8.1 | |
| `@astrojs/react` | 4.4 | 7.1 | |
| `react`, `react-dom` | 18.3 | 19.3 | plus `@types/react-dom` 19 |
| `tailwindcss` | 3.4 | 4.3 | `@astrojs/tailwind` replaced by `@tailwindcss/vite` |
| `@tailwindcss/typography` | 0.5 | 0.5 | works with v4 through `@plugin` |
| `astro-expressive-code` | 0.38 | 0.44 | supports Astro 7 |
| `react-icons` | 4.12 | 5.7 | 4 imports (`fi`, `fa`) |
| `js-yaml` | 4.3 | 5.5 | one use, `src/components/YamlLoader.js` |
| `katex`, `rehype-katex`, `remark-math` | 0.16 / 7 / 6 | **removed** | the math becomes MathML in Step 0 |

Astro 7's default Markdown processor (Sätteri) is used as is; the old
remark/rehype pipeline (`@astrojs/markdown-remark`) is not needed.

## Decisions (proposed; confirm before starting)

1. **Math as native MathML; Astro 7's default Markdown processor.** The
   only math is on four `/crypto-course/` pages (about 150 inline formulas
   and 11 displayed ones, all simple: exponents, mod, ×, φ). Convert it
   once to MathML, which browsers draw themselves (compared 2026-11-21:
   in Chrome it looks nearly identical to KaTeX), and drop `katex`,
   `remark-math`, `rehype-katex`, the KaTeX CSS and fonts, and
   `CryptoCourseMarkdown.astro`. Then nothing needs the old remark/rehype
   pipeline, so Astro 7 uses its default processor, Sätteri:
   expressive-code 0.44 supports it, and its smart punctuation turns `--`
   into an em dash as the site already does today (921 sentence dashes;
   command options like `--release` are all in code, which is never
   converted).
2. **Tailwind config:** convert to CSS (`@theme`) in the Tailwind step,
   keeping the same limited palette (`--color-*: initial`, then only the
   colors in `tailwind.config.cjs`). If that step gets messy, fall back to
   `@config "../../tailwind.config.cjs"` for this upgrade and convert later.
3. **Node:** stay on 22 (Astro 7 needs 22.23.4+; Netlify's `22` picks the
   latest 22.x). Moving to 24 to match FHTW is a separate, one-line change.
4. **`compressHTML`:** Astro 7 changes the default from `true` to `'jsx'`,
   which can remove spaces between inline elements. Set `compressHTML:
   true` to keep today's output, unless the comparison shows no difference.
5. **Browser support:** Tailwind 4 needs Safari 16.4+, Chrome 111+,
   Firefox 128+ (2023 or newer). Fine for students.
6. **Optional last step:** Astro's built-in CSP (`security.csp`, stable
   since 6.0) may let the CSP drop `'unsafe-inline'` for scripts by hashing
   Astro's inline scripts. Try it only if it works cleanly with the
   Netlify header CSP; otherwise leave the CSP as it is.

## How each step is checked

Before starting, build `main` and save it as the **baseline**
(`dist` copied to the scratch folder, not the repo). After each step:

1. `npm run build` passes, including the link check (no broken links).
2. **Compare every page to the baseline** (a script, kept out of the repo):
   visible text (tags stripped, whitespace normalized), the list of links
   and image sources, heading IDs (anchors), `<title>`, meta description and
   canonical. Zero differences, or each one explained. Hashed file names
   under `/_astro/` are expected to change and are ignored.
3. **Screenshots** of about 15 pages (front page, a current and an old
   semester home with the schedule grid, syllabus, a notes page with code,
   a page with images, a `/crypto-course/` page with math, a page with
   notices, the 404 page) at 1280 px and 390 px, before and after, compared
   side by side (and by pixel difference where useful).
4. On the deploy preview at the end: no horizontal scroll on every page at
   320/360/390/768 px; menus (dropdown and phone menu) work; no console or
   CSP errors; Lighthouse 100 on the same five pages as now.

## Order of work

One branch (`upgrade-deps`), one commit per step, a draft PR for a Netlify
preview. Each step must pass the checks before the next starts.
`@astrojs/tailwind` only supports Astro up to 5, so Tailwind moves first.

### Step 0: math to MathML (Astro 5 still)

- One-time script (kept out of the repo): for each `$...$` and `$$...$$`
  in the four pages (`crypto-course/projects/diffie-hellman.mdx`,
  `projects/rsa.mdx`, `homework/diffie-hellman.mdx`,
  `homework/rsa-keys.mdx`), write KaTeX's MathML-only output
  (`output: "mathml"`, `displayMode` for `$$`) into the page. KaTeX keeps
  each formula's TeX in an `<annotation>`, so it can be regenerated later.
  In MDX, braces in that TeX must be escaped (`&#123;` / `&#125;`) so they
  aren't read as JSX expressions.
- Remove `remark-math` and `rehype-katex` from `astro.config.mjs`, the
  three packages, and `CryptoCourseMarkdown.astro` (those pages go back to
  `SemesterMarkdown.astro`).
- Check: the four pages' text matches the baseline apart from the math
  markup; no `$` delimiters or TeX left showing; screenshots of the math
  in **Chrome, Safari and Firefox** (each uses its own math font). If one
  of them looks poor, stop and decide before going on.
- Optional while there: the 24 number ranges written `1--5` render as
  "1—5" (em dash); writing them as "1–5" (en dash) is more correct.

### Step 1: small packages (Astro 5 still)

- `react` / `react-dom` 19 and `@types/react-dom` 19; `@astrojs/react`
  stays at 4.4 for now (it accepts React 19).
- `react-icons` 5: check that `FiAlertTriangle`, `FiInfo` and the other
  imported icons still exist.
- `js-yaml` 5: check `load()` in `YamlLoader.js` still behaves the same.
- `astro-expressive-code` 0.38 to 0.44: compare code blocks closely
  (frames, copy button, colors, wrapping).

### Step 2: Tailwind 4 (Astro 5 still)

- Remove `@astrojs/tailwind`; add `tailwindcss` 4 and `@tailwindcss/vite`
  (in `vite.plugins` in `astro.config.mjs`). Try `npx @tailwindcss/upgrade`
  first and review its diff.
- `src/assets/base.css`: `@import "tailwindcss";`, `@plugin
  "@tailwindcss/typography";`, the `@theme` palette, and the existing
  `@layer base` heading sizes.
- Port the typography overrides (no quote marks on blockquotes, no
  backticks around inline code, link color and weight, heading margins
  and sizes) as plain CSS under `.prose`.
- Known traps to check in the screenshots: default border color is now
  `currentColor` (was gray-200), `ring` is 1px (was 3px), `shadow`,
  `rounded` and `blur` sizes renamed (`shadow-sm` to `shadow-xs`, and
  so on), buttons get `cursor: default`, `hover:` applies only on devices
  with a mouse, `space-y-*` selectors changed, `outline-none` renamed.
- Check that classes outside the palette (e.g. `green-*`) still don't
  exist, and that `bg-transparent` / `text-current` still work.
- Delete `tailwind.config.cjs` once nothing uses it.

### Step 3: Astro 6

- `npx @astrojs/upgrade` (moves `astro`, `@astrojs/mdx`, `@astrojs/react`
  together); then build.
- Check: Vite 7 and `vite.ssr.noExternal: ["react-icons"]` (may no longer
  be needed); Shiki 4 with `markdown.shikiConfig`; **heading IDs** (Astro 6
  keeps trailing hyphens, which could change anchors; the comparison checks
  this and the link check catches broken in-page links); `Astro.url` may
  be partly decoded (canonical URLs); images (Astro 6 never upscales and
  changes cropping); `<script>`/`<style>` now render in source order.

### Step 4: Astro 7

- `npx @astrojs/upgrade` again. Astro 7 switches Markdown and MDX to
  Sätteri. Remove the now-unused `markdown.remarkPlugins` /
  `rehypePlugins` settings; check what replaces `markdown.shikiConfig`
  (themes, `wrap`) under Sätteri, though code blocks are rendered by
  expressive-code, which has its own Sätteri plugin.
- Compare dashes, quotes and ellipses against the baseline: Sätteri's
  smart punctuation should match today's output (`--` to an em dash); any
  difference shows up in the text comparison. Heading IDs may also
  change; the comparison and the link check catch that.
- Rust compiler: unclosed tags are errors and invalid nesting (a `<div>`
  inside a `<p>`) is no longer fixed up; fix any `.astro` files it rejects
  (there are only 8 `.astro` files).
- `compressHTML` (decision 4).
- Check that layouts still get `Astro.props.frontmatter` and
  `Astro.props.headings` from MDX pages (page titles come from the first
  heading via `src/layouts/title.js`); the comparison of `<title>` catches
  this.
- Math: the MathML from Step 0 is unchanged (it's raw HTML in the page,
  so the processor doesn't touch it).

### Step 5 (optional): built-in CSP

- Try `security: { csp: true }` and see whether Astro emits hashes for its
  inline scripts on a static build. If so, move to a hash-based CSP and
  drop `'unsafe-inline'` from `script-src` in `netlify.toml`. Check every
  page type for CSP errors on the preview.

### Step 6: finish

- Update `.nvmrc` / `netlify.toml` if the Node version changed, the README
  (commands, Tailwind config location), and this plan's status with an
  "As built" section.
- Merge after checking the preview; check production headers and
  Lighthouse.

## Risks and unknowns to check first

- How MathML looks in Safari and Firefox (Step 0 checks; Chrome is fine).
- Whether MDX passes raw `<math>` markup through unchanged in both Astro 5
  and Astro 7 (Step 0 and Step 4 comparisons).
- What replaces `markdown.shikiConfig` under Sätteri, and whether
  expressive-code's Sätteri plugin produces the same code blocks.
- Whether `Astro.props.headings` still reaches the layout for MDX pages in
  Astro 7.
- Whether expressive-code 0.44 changes how code blocks look (it has
  explicit Sätteri support, checked in its 0.44.4 source).
- The Tailwind palette and typography port: most likely source of small
  visual differences.
- If any step goes badly, stop there: each step is its own commit, and the
  site on `main` is untouched until the merge.

## Sources

Astro upgrade guides for v6 and v7, Astro's Sätteri and MDX docs, the
Tailwind v4 upgrade guide and Astro install guide, and the
`@tailwindcss/typography` README (read 2026-11-21); package versions and
peer dependencies from npm on the same day.
