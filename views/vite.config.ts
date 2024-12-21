import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  const config = {
    plugins: [svelte({ preprocess: vitePreprocess() })],
    resolve: {
      alias: {
        "$lib/": fileURLToPath(new URL("./src/lib/", import.meta.url)),
      },
    },
    build: {
      outDir: "../static/",
      manifest: 'manifest.json',
      emptyOutDir: true,
      rollupOptions: {
        input: "/src/main.js",
        output: {
          entryFileNames: "[name].js",
          assetFileNames: "[name].[ext]",
        }
      },

    }
  };
  return {
    ...config,
  };
});
