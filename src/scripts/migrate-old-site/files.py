"""Copy the old site's files, once each, and record old -> new links."""

import hashlib
import shutil
import subprocess
from collections import defaultdict

from common import LECTURE_DIRS, OLD, WEB, load_links, save_links

LECTURES = WEB / "public/lectures/crypto-course"
CODE = WEB / "public/code/crypto-course"
IMAGES = WEB / "src/images/crypto-course"

# Handouts: old file -> project folder. cracklib.txt (15.6 MB) is not copied.
HANDOUTS = {
    "passwd.txt": "password-cracking", "shadow.txt": "password-cracking",
    "plaintext.txt": "aes-library",
    "dh.zip": "diffie-hellman",
    "stacksmashing/sample3.tar": "buffer-overflow",
    "overflow.c": "buffer-overflow-2023", "overflow2.c": "buffer-overflow-2023",
    "overflow": "buffer-overflow-2023", "shell_test.c": "buffer-overflow-2023",
    "secrets/fortune_static": "extracting-secrets", "secrets/fortunes.enc": "extracting-secrets",
    "secret_treasure": "extracting-secrets-2023", "treasures.enc": "extracting-secrets-2023",
}

# Images actually used by pages. Staff photos and the TA office-hours
# schedule (tasched.png) are not copied; unused VM screenshots are skipped.
IMAGES_USED = ["func1.png", "func2.png", "vm/1_import.png", "vm/2_select.png",
               "vm/3_options.png", "vm/4_progress.png", "vm/5_memory.png", "vm/vm_7.png"]


# Google Docs and Slides the old pages linked to, saved as PDFs (exported
# 2026-11-21; sharing links rot). id -> (kind, file name).
GOOGLE = {
    "1FnqqExqirZTQYsI3kN_74OfyiQKBoIsNShXk2ApcNrI": ("presentation", "stack-frame-layout.pdf"),
    "1KLlm3jnEW-yql4qrx4Ud8H3x0EmsJDeKNLKnfZ3Ogk8": ("presentation", "stack-frame-layout-64bit.pdf"),
    "1i2TvaLXZjWtZubOm-7sNVrbmnNg3ji1fQ9XmaWzE_n8": ("presentation", "hash-attack-discussion.pdf"),
    "19HfSDfiPJxaC-snRp-C2gw466UzeYlOtPEpeh2679CE": ("presentation", "mac-attack-discussion.pdf"),
    "1eqFB1IklngE5x2iEVxkU2q9cV-eFH7JJPF7TK9AE0BM": ("presentation", "multifactor-auth-and-password-vaults.pdf"),
    "13vkvFGAOcujmaiWLPLdw0gdQE-5psRy2x2pbb98kXHk": ("presentation", "finite-field-multiply-examples.pdf"),
    "1C85G1FQjeE693p9ShNSFOdyW7yg1udRxkj9okmOamjc": ("document", "tls-cipher-suite-example.pdf"),
    "1Te0Z-AnMGX9aECaZQGG5kzO8hQKtWOO1a7ksLOzlYmY": ("document", "midterm-1-study-guide-winter2022.pdf"),
    "1HZtcQ4YfiKS62g9wICPhCPvmA0DPhzl7pT7JCm4St3s": ("document", "midterm-2-study-guide-winter2022.pdf"),
    "1tUISx0gQz1OkKihHag4WBzRKlo5hgIB_-ApwGypFmJg": ("document", "midterm-1-study-guide-fall2023.pdf"),
    "1suND4Z-r1uDvHMj8fSCWAyScR_1gjavcNu8SFtjPcCQ": ("document", "midterm-2-study-guide-fall2023.pdf"),
}


def google(links):
    """Download each Google file as PDF (skipped if already saved)."""
    import urllib.request
    folder = LECTURES / "docs"
    folder.mkdir(parents=True, exist_ok=True)
    for doc_id, (kind, name) in GOOGLE.items():
        target = folder / name
        if not target.exists():
            url = (f"https://docs.google.com/presentation/d/{doc_id}/export/pdf" if kind == "presentation"
                   else f"https://docs.google.com/document/d/{doc_id}/export?format=pdf")
            target.write_bytes(urllib.request.urlopen(url, timeout=60).read())
        links[f"google:{doc_id}"] = f"/lectures/crypto-course/docs/{name}"


def md5(path):
    return hashlib.md5(path.read_bytes()).hexdigest()


def lectures(links):
    versions = defaultdict(dict)  # base name -> hash -> (first semester, source, [old paths])
    for folder, semester in LECTURE_DIRS:
        for pdf in sorted((OLD / "static/lectures" / folder).glob("*.pdf")):
            base = pdf.stem.removesuffix("-f18")
            entry = versions[base].setdefault(md5(pdf), [semester, pdf, []])
            entry[2].append(f"/static/lectures/{folder}/{pdf.name}")
    LECTURES.mkdir(parents=True, exist_ok=True)
    for base, by_hash in sorted(versions.items()):
        for semester, source, old_paths in by_hash.values():
            name = f"{base}.pdf" if len(by_hash) == 1 else f"{base}-{semester}.pdf"
            if not (LECTURES / name).exists():  # keep edited copies (e.g. shrunk PDFs)
                shutil.copy2(source, LECTURES / name)
            for old in old_paths:
                links[old] = f"/lectures/crypto-course/{name}"
    return sum(len(v) for v in versions.values())


def readings(links):
    (LECTURES / "readings").mkdir(parents=True, exist_ok=True)
    for pdf in sorted((OLD / "static/pubs").glob("*.pdf")):
        shutil.copy2(pdf, LECTURES / "readings" / pdf.name)
        links[f"/static/pubs/{pdf.name}"] = f"/lectures/crypto-course/readings/{pdf.name}"


def handouts(links):
    for old, project in HANDOUTS.items():
        target = CODE / project / old.split("/")[-1]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OLD / "static/files" / old, target)
        links[f"/static/files/{old}"] = f"/code/crypto-course/{project}/{target.name}"


def images(links):
    for old in IMAGES_USED:
        source = OLD / "static/img" / old
        target = IMAGES / old
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.stat().st_size > 300_000:  # large screenshots: smaller WebP
            target = target.with_suffix(".webp")
            subprocess.run(["cwebp", "-quiet", "-q", "82", "-resize", "1600", "0",
                            str(source), "-o", str(target)], check=True)
        else:
            shutil.copy2(source, target)
        links[f"/static/img/{old}"] = f"@/images/crypto-course/{target.relative_to(IMAGES)}"


if __name__ == "__main__":
    links = load_links()
    print("lecture PDFs:", lectures(links))
    readings(links)
    handouts(links)
    images(links)
    google(links)
    save_links(links)
    print("links recorded:", len(links))
