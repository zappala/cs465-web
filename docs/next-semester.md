# Next semester: make the updated crypto pages the only versions

Written 2026-11-17, after the Fall 2026 mid-semester update.

## Background

In November 2026 (Fall 2026), the Encrypted Communication project and the
crypto material were updated to current Rust crates and RSA-OAEP/RSA-PSS. To
avoid changing things under students mid-semester, the original Fall 2026
pages were kept and updated versions were added next to them:

| Original (v1) | Updated (v2) |
| --- | --- |
| `projects/encrypted-communication.mdx` (handout `public/code/encrypted-communication/v1/`) | `projects/encrypted-communication-v2.mdx` (handout `public/code/encrypted-communication/v2/`) |
| `notes/public-key-cryptography.mdx` | `notes/public-key-cryptography-v2.mdx` |
| `notes/learning-rust-abbreviated.mdx` | `notes/learning-rust-abbreviated-v2.mdx` |
| Slides: `Symmetric Encryption and Public Key Cryptography.pdf` | `Symmetric Encryption and Public Key Cryptography (updated).pdf` |

Each original page has a `VersionNotice` pointing to its update, and the Fall
2026 schedule lists both versions. Starting next semester, only the updated
versions should exist, under the plain names.

Related repos: `BYU-CS465/encrypted-communication` (handout, solution,
server; build the handout zip with its `scripts/make-handout.sh`) and
`BYU-CS465/rust-cryptography` (the class examples; the `2024` tag holds the
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
   ```

3. **Remove the version notices and "(updated)" labels** in those three pages:
   - delete the `import VersionNotice ...` line and the
     `<VersionNotice ...>...</VersionNotice>` block;
   - project page: change the heading "Project: Encrypted Communication
     (updated)" to "Project: Encrypted Communication";
   - public key notes: delete the `title: Public Key Cryptography (updated)`
     frontmatter line;
   - Learning Rust notes: change the frontmatter line to
     `title: Learning Rust (abbreviated)`.

   Check (should print nothing):
   ```sh
   grep -rn "VersionNotice\|-v2\|(updated)\|/fall2026/" src/pages/winter2027
   ```

4. **Schedule** (`src/data/winter2027/schedule.yaml`): remove the
   "(updated)" lecture and slide entries, and make `project` a single entry
   again pointing at `/projects/encrypted-communication`. Check (should print
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
   - `public/code/encrypted-communication/v1/` and `v2/` (older semesters
     link to v1; the new project page links to v2);
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

8. `npm run build`, click through with `npm run dev`, then commit and push.
