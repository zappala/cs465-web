// Runs after `astro build` (see "build" in package.json):
//
// 1. Checks every internal link and file reference (href/src) in dist/ and
//    fails the build if any target is missing, so a broken link never
//    deploys. Also fails on <a> tags with no href.
// 2. Writes dist/sitemap.xml listing every page except the 404 page and
//    pages marked noindex.
//
// Run it by itself after a build with: node src/scripts/postbuild.mjs

import fs from "node:fs";
import path from "node:path";

const SITE = "https://cs465.zappala.org";
const dist = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../../dist");

function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const full = path.join(dir, entry.name);
    return entry.isDirectory() ? walk(full) : [full];
  });
}

const files = walk(dist);
const htmlFiles = files.filter((f) => f.endsWith(".html"));

// URL path of a built page: dist/a/b/index.html -> /a/b/
function pagePath(file) {
  const rel = "/" + path.relative(dist, file).split(path.sep).join("/");
  return rel.endsWith("/index.html") ? rel.slice(0, -"index.html".length) : rel;
}

function exists(urlPath) {
  const target = path.join(dist, urlPath);
  if (fs.existsSync(target) && fs.statSync(target).isFile()) return true;
  if (fs.existsSync(path.join(target, "index.html"))) return true;
  return fs.existsSync(target + ".html");
}

const decode = (s) =>
  s.replace(/&amp;/g, "&").replace(/&#34;|&quot;/g, '"').replace(/&#39;/g, "'");

let linkCount = 0;
const broken = new Map(); // target -> Set of pages
const noHref = [];

for (const file of htmlFiles) {
  const page = pagePath(file);
  const html = fs.readFileSync(file, "utf8");

  for (const tag of html.match(/<a\b[^>]*>/g) ?? []) {
    if (!/\shref=/.test(tag) && !/\s(id|name)=/.test(tag)) noHref.push(`${page}: ${tag.slice(0, 80)}`);
  }

  for (const [, raw] of html.matchAll(/\s(?:href|src)="([^"]+)"/g)) {
    const url = decode(raw);
    if (/^([a-z][a-z0-9+.-]*:|#|\/\/)/i.test(url)) continue; // external, mailto:, data:, anchors
    let target = decodeURIComponent(url.split(/[?#]/)[0]);
    if (!target) continue;
    if (!target.startsWith("/")) {
      const base = page.endsWith("/") ? page : path.posix.dirname(page) + "/";
      target = path.posix.normalize(base + target);
    }
    linkCount++;
    if (!exists(target)) {
      if (!broken.has(target)) broken.set(target, new Set());
      broken.get(target).add(page);
    }
  }
}

// Sitemap
const pages = htmlFiles
  .filter((f) => path.basename(f) === "index.html")
  .filter((f) => !/<meta name="robots" content="noindex"/.test(fs.readFileSync(f, "utf8")))
  .map(pagePath)
  .sort();
const sitemap =
  '<?xml version="1.0" encoding="UTF-8"?>\n' +
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
  pages.map((p) => `  <url><loc>${SITE}${encodeURI(p)}</loc></url>`).join("\n") +
  "\n</urlset>\n";
fs.writeFileSync(path.join(dist, "sitemap.xml"), sitemap);
console.log(`postbuild: sitemap.xml with ${pages.length} pages`);

console.log(`postbuild: ${linkCount} internal links checked in ${htmlFiles.length} pages`);
if (broken.size || noHref.length) {
  for (const [target, from] of broken) {
    console.error(`  broken: ${target}  (from ${[...from].slice(0, 3).join(", ")}${from.size > 3 ? ", ..." : ""})`);
  }
  for (const line of noHref) console.error(`  <a> without href: ${line}`);
  console.error(`postbuild: ${broken.size} broken link targets, ${noHref.length} links without href`);
  process.exit(1);
}
console.log("postbuild: no broken links");
