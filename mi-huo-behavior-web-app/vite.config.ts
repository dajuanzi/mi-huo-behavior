import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    //port: 8000,
    proxy: {
      "/generate_confusion": {
        target: "http://127.0.0.1:8000", // Backend server
        changeOrigin: true,
        rewrite: (path) =>
          path.replace(/^\/generate_confusion/, "/generate_confusion"),
      },
    },
  },
});
