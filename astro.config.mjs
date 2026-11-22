import { defineConfig } from 'astro/config';
import mdx from "@astrojs/mdx";
import tailwindcss from "@tailwindcss/vite";
import react from "@astrojs/react";

import expressiveCode from "astro-expressive-code";

// https://astro.build/config
export default defineConfig({
  site: "https://cs465.zappala.org",
  // Astro 7's default ('jsx') drops whitespace with a line break between
  // tags, which can run words together in .astro templates; keep Astro 6's.
  compressHTML: true,
  security: {
    csp: {
      styleDirective: {
        resources: ["'self'", { resource: "'unsafe-inline'", kind: "attribute" }],
      },
    },
  },
  integrations: [expressiveCode(), mdx(), react()],
  vite: {
    plugins: [tailwindcss()],
  }
});