// Build a link for a menu or schedule entry.
//
// Links in a semester's menu.yaml and schedule.yaml are relative to the
// semester (e.g. "/projects/linux" becomes "/fall2026/projects/linux").
// Links that already point somewhere else are used as they are:
//   - external links ("https://...")
//   - pages shared by several semesters, which live outside any semester
//     folder (the 2018-2023 course's pages under "/crypto-course/")
const SHARED = "/crypto-course";

export function resolveLink(prefix, url) {
  if (!url) return url;
  if (/^[a-z]+:/i.test(url)) return url;
  if (url === SHARED || url.startsWith(SHARED + "/")) return url;
  return prefix + (url.startsWith("/") ? url : "/" + url);
}
