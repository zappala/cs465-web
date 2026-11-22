# One-time scripts: move the 2018-2023 site into this one

See `docs/old-site-migration-plan.md`. These read the old site from
`~/Repos/cs465/old/cs465` (override with `OLD_SITE=...`) and write into this
repo. Delete this folder when the migration is done.

- `files.py`: copies the deduplicated lecture PDFs, readings, handouts and
  images, and writes `links.json` (old path -> new path) for the other
  scripts.
- `shrink_pdf_images.py`: downsamples a PDF's large images without touching
  its text (Ghostscript's `pdfwrite` garbled the text layer). Used once:
  `uv run --with pikepdf --with pillow python shrink_pdf_images.py
  <old>/static/lectures/w19/Introduction.pdf
  public/lectures/crypto-course/Introduction-winter2019.pdf 1800`
  (10.9 MB -> 0.31 MB, text unchanged).
