import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        surface: {
          DEFAULT: "#0F1117",
          raised: "#161B22",
          overlay: "#1C2128",
        },
        "on-surface": {
          DEFAULT: "#E6EDF3",
          muted: "#8B949E",
        },
        border: {
          DEFAULT: "#30363D",
          emphasis: "#484F58",
        },
        primary: {
          DEFAULT: "#2F81F7",
          hover: "#388BFD",
        },
        accent: {
          DEFAULT: "#56D364",
          hover: "#6EE77A",
        },
        error: {
          DEFAULT: "#F85149",
          subtle: "#3D1D20",
        },
        warning: {
          DEFAULT: "#D29922",
          subtle: "#2E2111",
        },
        success: {
          DEFAULT: "#3FB950",
          subtle: "#122117",
        },
        info: {
          DEFAULT: "#58A6FF",
          subtle: "#121D2F",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "-apple-system", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "Consolas", "monospace"],
      },
      borderRadius: {
        sm: "4px",
        md: "6px",
        lg: "8px",
      },
    },
  },
  plugins: [],
};

export default config;
