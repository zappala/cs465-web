import { defineConfig } from 'astro/config';
import mdx from "@astrojs/mdx";
import tailwindcss from "@tailwindcss/vite";
import react from "@astrojs/react";

import expressiveCode from "astro-expressive-code";

// https://astro.build/config
export default defineConfig({
  site: "https://cs465.zappala.org",
  integrations: [expressiveCode(), mdx(), react()],
  vite: {
    plugins: [tailwindcss()],
    ssr: {
      noExternal: ["react-icons"]
    }
  },
  markdown: {
    shikiConfig: {
      // Choose from Shiki's built-in themes (or add your own)
      // https://shiki.style/themes
      // Alternatively, provide multiple themes
      // See note below for using dual light/dark themes
      theme: 'github-light',
      themes: {
        light: 'github-light',
        dark: 'github-dark'
      },
      // Enable word wrap to prevent horizontal scrolling
      wrap: true,
      // Add custom transformers: https://shiki.style/guide/transformers
      // Find common transformers: https://shiki.style/packages/transformers
      transformers: []
    }
  }
});