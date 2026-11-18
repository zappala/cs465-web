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

11. `npm run build`, click through with `npm run dev`, then commit and push.

## Also worth doing between semesters

- **Major package upgrades** (noted 2026-11-17): the site is on Astro 5.18
  and Tailwind 3.4 (the latest within those major versions). Astro 7 and
  Tailwind 4 are current. The remaining `npm audit` advisories need these
  upgrades. Tailwind 4 replaces `@astrojs/tailwind` with `@tailwindcss/vite`
  and moves the config into CSS, so plan time for it. Before and after,
  build the site and compare every page's text and links, and check the
  schedule, a notes page, and the phone menu visually.
