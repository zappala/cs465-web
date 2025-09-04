/** @type {import('tailwindcss').Config} */
const colors = require("tailwindcss/colors");

const round = (num) =>
  num
    .toFixed(7)
    .replace(/(\.[0-9]+?)0+$/, "$1")
    .replace(/\.0$/, "");
const rem = (px) => `${round(px / 16)}rem`;
const em = (px, base) => `${round(px / base)}em`;

module.exports = {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}"],
  theme: {
    colors: {
      transparent: "transparent",
      current: "currentColor",
      default: "#1a202c",
      byu: "#002e5d",
      red: "#b22222",
      lightblue: "#3182ce",
      yellow: "#ffcd00",
      bluey: "#182b49",
      red: colors.red,
      blue: colors.blue,
      sky: colors.sky,
      slate: colors.slate,
      gray: colors.gray,
      white: colors.white,
    },

    extend: {
      fontFamily: {
        young: ['"Young Serif"', "serif"],
        playfair: ['"Playfair Display"', "serif"],
      },
      typography: {
        DEFAULT: {
          css: {
            "blockquote p:first-of-type::before": { content: "none" },
            "blockquote p:first-of-type::after": { content: "none" },
            "code::before": {
              content: '""',
            },
            "code::after": {
              content: '""',
            },
            code: {
              color: "#b22222",
            },
            "> :first-child": {
              marginTop: em(8, 14),
            },
            h1: {
              marginTop: em(16, 14),
            },
            a: {
              fontWeight: "400",
              color: "#3182ce",
            },
            h3: {
              fontSize: "1.1em",
            },
          },
        },
      },
    },
  },

  plugins: [require("@tailwindcss/typography")],
};
