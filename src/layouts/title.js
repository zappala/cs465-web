// The title for a page's browser tab: the page's `title` frontmatter if it has
// one, otherwise its first `#` heading. Astro passes `frontmatter` and
// `headings` to the layout of a Markdown/MDX page.
export function pageTitle(props) {
  if (props.frontmatter?.title) return props.frontmatter.title;
  return props.headings?.find((heading) => heading.depth === 1)?.text;
}
