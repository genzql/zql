import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import monacoEditorPlugin from "vite-plugin-monaco-editor";

import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    host: "0.0.0.0",
    port: 3000,
  },
  preview: {
    port: 3000,
  },

  plugins: [
    react(),
    ((monacoEditorPlugin as any).default as typeof monacoEditorPlugin)({}), // https://github.com/vdesjs/vite-plugin-monaco-editor/issues/21
  ],

  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
