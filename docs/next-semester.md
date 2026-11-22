# Next semester: make the updated crypto pages the only versions

Written 2026-11-17, after the Fall 2026 mid-semester update.

## Background

In November 2026 (Fall 2026), the Encrypted Communication project and the
crypto material were updated to current Rust crates and RSA-OAEP/RSA-PSS, and
the Cracking Password Vaults project got new vaults that wrap a random vault
key (600,000 PBKDF2 rounds, 16-byte salt). To avoid changing things under students mid-semester, the original Fall 2026
pages were kept and updated versions were added next to them:

| Original (v1) | Updated (v2) |
| --- | --- |
| `projects/encrypted-communication.mdx` (handout `public/code/encrypted-communication/v1/`) | `projects/encrypted-communication-v2.mdx` (handout `public/code/encrypted-communication/v2/`) |
| `notes/public-key-cryptography.mdx` | `notes/public-key-cryptography-v2.mdx` |
| `notes/learning-rust-abbreviated.mdx` | `notes/learning-rust-abbreviated-v2.mdx` |
| `projects/cracking-password-vaults.mdx` (handout `public/code/cracking-password-vaults/v1/`) | `projects/cracking-password-vaults-v2.mdx` (handout `public/code/cracking-password-vaults/v2/`) |
| Slides: `Symmetric Encryption and Public Key Cryptography.pdf` | `Symmetric Encryption and Public Key Cryptography (updated).pdf` |

Each original page has a `VersionNotice` pointing to its update, and the Fall
2026 schedule lists both versions. Starting next semester, only the updated
versions should exist, under the plain names.

Related repos: `BYU-CS465/encrypted-communication` (handout, solution,
server; build the handout zip with its `scripts/make-handout.sh`),
`BYU-CS465/cracking-password-vaults` (setup, handout, solution; its README
has the per-semester steps), and `BYU-CS465/rust-cryptography` (the class examples; the `2024` tag holds the
original code that the Fall 2026 v1 pages link to).

## Steps

Use the real name of the new semester in place of `winter2027` / `w2027`.

1. **Copy the semester** as usual:
   ```sh
   cp -R src/pages/fall2026 src/pages/winter2027
   cp -R src/data/fall2026 src/data/winter2027
   ```
   Update `menu.yaml` (semester name), the dates in `schedule.yaml`, the
   "Current Semester" button in `src/pages/index.mdx`, and the current
   semester link in `src/pages/404.astro`.

2. **Replace each original page with its updated page** (`mv` overwrites the
   original, which is what we want):
   ```sh
   cd src/pages/winter2027
   mv projects/encrypted-communication-v2.mdx projects/encrypted-communication.mdx
   mv notes/public-key-cryptography-v2.mdx notes/public-key-cryptography.mdx
   mv notes/learning-rust-abbreviated-v2.mdx notes/learning-rust-abbreviated.mdx
   mv projects/cracking-password-vaults-v2.mdx projects/cracking-password-vaults.mdx
   ```

3. **Remove the version notices and "(updated)" labels** in those four pages:
   - delete the `import VersionNotice ...` line and the
     `<VersionNotice ...>...</VersionNotice>` block;
   - project pages: drop " (updated)" from the headings "Project: Encrypted
     Communication (updated)" and "Project: Cracking Password Vaults
     (updated)";
   - public key notes: delete the `title: Public Key Cryptography (updated)`
     frontmatter line;
   - Learning Rust notes: change the frontmatter line to
     `title: Learning Rust (abbreviated)`.

   Check (should print nothing):
   ```sh
   grep -rn "VersionNotice\|-v2\|(updated)\|/fall2026/" src/pages/winter2027
   ```

4. **Schedule** (`src/data/winter2027/schedule.yaml`): remove the
   "(updated)" lecture and slide entries, and make each `project` a single
   entry again, pointing at `/projects/encrypted-communication` and
   `/projects/cracking-password-vaults`. Check (should print
   nothing):
   ```sh
   grep -n "updated\|-v2" src/data/winter2027/schedule.yaml
   ```

5. **Slides:** copy
   `~/Dropbox/Teaching/cs465/slides/Symmetric Encryption and Public Key Cryptography (updated).pdf`
   to `public/lectures/w2027/Symmetric Encryption and Public Key Cryptography.pdf`.
   In Dropbox, consider renaming the updated `.pptx` to the plain name and
   keeping the original as `... (2024 version).pptx`.

6. **Keep these as they are:**
   - `public/code/encrypted-communication/v1/` and `v2/`, and
     `public/code/cracking-password-vaults/v1/` and `v2/` (older semesters
     link to v1; the new project pages link to v2);
   - `src/components/VersionNotice.jsx` and the list-of-projects support in
     `src/components/GridSchedule.jsx` (useful the next time something is
     updated mid-semester);
   - the `2024` tag in rust-cryptography (the Fall 2026 v1 pages link to it).

7. **Rust versions:** check the
   [Rust book's title page](https://doc.rust-lang.org/book/title-page.html).
   If it now assumes a newer Rust than 1.98, update "Rust 1.98 or newer" on
   the project page, the notes, the handout README, and the rust-cryptography
   READMEs. Run `cargo update` in rust-cryptography and in
   encrypted-communication if crates have new releases (then rebuild the
   server binaries and the handout zip).

8. **Zip submissions:** handouts are zips now, so submissions should be too.
   The Encrypted Communication v2 page already asks for a zip (`cargo clean`,
   then `zip -r ... -x '*/target/*' '*/.git/*'` or Explorer's Compress to ZIP
   file). Copy that Submission section to any other project page that still
   says `tar`. Check:
   ```sh
   grep -rln "czvf\|tar --exclude\|tar file" src/pages/winter2027
   ```

9. **New password vaults** (do this every semester, never during one): in
   `~/Repos/cs465/cracking-password-vaults`, run `scripts/new-vaults.sh`, then
   `scripts/make-handout.sh`, copy `cracking-password-vaults.zip` to
   `public/code/cracking-password-vaults/v2/`, and commit both repos. New
   vaults stop students from reusing earlier semesters' answers. The repo's
   README has details.

10. **Vaults rubric:** consider whether to give credit for correctly reporting
    the 3 breach vaults that can't be cracked (currently 40 points: 10 each
    for the practice vault and the 3 crackable breach vaults).

11. **Pin the Juice Shop version** on the Web Exploit and Patch page, so a
    new release can't change the challenges mid-semester. Find the newest
    `vX.Y.Z` tag at https://hub.docker.com/r/bkimminich/juice-shop/tags, run
    it, and check that the assigned challenges still exist (and which have
    coding challenges, for the extra credit). Then change the command to, for
    example:
    ```bash
    docker run --rm -p 127.0.0.1:3000:3000 -e NODE_ENV=unsafe bkimminich/juice-shop:v20.4.0
    ```
    (v20.4.0, released 2026-11-08, was checked on 2026-11-17: all 7
    challenges present; all but Reflected XSS have coding challenges;
    `NODE_ENV=unsafe` is still needed for Reflected XSS and API-only XSS.)

12. `npm run build`, click through with `npm run dev`, then commit and push.

## Also worth doing between semesters

- **Major package upgrades** (noted 2026-11-17): the site is on Astro 5.18
  and Tailwind 3.4 (the latest within those major versions). Astro 7 and
  Tailwind 4 are current. The remaining `npm audit` advisories need these
  upgrades. Tailwind 4 replaces `@astrojs/tailwind` with `@tailwindcss/vite`
  and moves the config into CSS, so plan time for it. Before and after,
  build the site and compare every page's text and links, and check the
  schedule, a notes page, and the phone menu visually.

- **Sync assignments and the syllabus to Canvas** (noted 2026-11-17): a
  plan to push due dates, points, and links to the website's pages from
  `schedule.yaml` to Canvas, and to sync the syllabus, is in
  [canvas-sync-plan.md](canvas-sync-plan.md). Not started.

- **Consider an LLM security challenge in Web Exploit and Patch** (noted
  2026-11-17): Juice Shop now has "Chatbot Prompt Injection" (difficulty 2:
  trick the shop's chatbot into giving a coupon code its policy forbids) and
  "Greedy Chatbot Manipulation" (difficulty 3). Adding one would also mean
  covering LLM security (prompt injection and related attacks) in class, plus
  updating the rubric and `submission.md`.

- **Rework the Exploit and Patch project** (noted 2026-11-17): move it to
  64-bit, replace the confusing problem 5 with a new heap-overflow problem, add
  a shellcode extra-credit problem, and adopt a shared x86-64 Codespaces +
  local-Docker devcontainer as the default environment. Full plan:
  `~/Repos/cs465/exploit-and-patch-update-plan.md`; the environment analysis is
  in [exploit-env-plan.md](exploit-env-plan.md).

- **Switch all handouts and turn-ins to zip** (noted 2026-11-17): handouts are
  zips now (Encrypted Communication, Cracking Password Vaults, and the Exploit
  and Patch download already switched). For each remaining project, publish the
  handout as `.zip` and update the page's download link and wording, and make
  the Submission section ask for a `.zip` (see step 8 above for the student
  command). Check for stragglers:
  ```sh
  grep -rln "tar.gz\|czvf\|tar --exclude\|tar file" src/pages public/code
  ```

- **Add a "what you'll need" section to the syllabus plus a setup sheet** (noted
  2026-11-17): the syllabus should list the technology students use during the
  semester (a Linux environment — Codespaces / VM / VPS / department machines;
  Rust via `rustup`; Docker for Juice Shop; a GitHub account, with student
  verification for Codespaces; a browser with dev tools / Burp) and link a
  single **setup sheet** they can follow before the semester to install and
  verify everything early. Keep the setup sheet as the one place these
  instructions live, and have the per-project pages link to it rather than
  repeating setup steps. Coordinate with the environment rollout in
  [exploit-env-plan.md](exploit-env-plan.md).

- **Update the lecture notes from the slides** (noted 2026-11-17): the slide
  decks (`~/Dropbox/Teaching/cs465/slides`, exported to
  `public/lectures/`) are more recent than the online notes in
  `src/pages/<semester>/notes/*.mdx`. Between semesters, review the notes
  against the current slides and bring anything out of date into line.

- **Upgrade the site's dependencies** (noted 2026-11-21): planned in
  [dependency-upgrade-plan.md](dependency-upgrade-plan.md).

- **Decide whether to move large files to object storage (R2)** (moved here
  from `~/Repos/notes/TODO.md` on 2026-11-21). The repo is about 171 MB,
  mostly PDFs and handouts in `public/lectures` and `public/code`; the
  largest are a 23 MB card deck and a 17 MB zip. GitHub is fine with this
  (it suggests under 1 GB). R2 would cost nothing at this size but adds a
  bucket, a redirect, a manifest, scripts and a backup (the FHTW setup).
  Revisit if the repo nears 1 GB or video/audio is added. The R2 free tier
  (10 GB) is per Cloudflare account, shared with `fhtw-conf`.
  Small step any time: `public/lectures/w2026/social_engineering.pdf` and
  `public/lectures/crypto-course/social_engineering.pdf` are the same 4.6 MB
  file; point `src/data/winter2026/schedule.yaml` at the crypto-course copy
  and delete the other.
