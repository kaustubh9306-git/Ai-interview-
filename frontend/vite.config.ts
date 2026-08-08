import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Optional dev proxy: if the backend's CORS configuration ever blocks
    // http://localhost:5173, uncomment this and set VITE_API_BASE_URL to ""
    // so requests go through Vite instead of hitting the backend directly.
    // proxy: {
    //   "/api": {
    //     target: "http://127.0.0.1:8000",
    //     changeOrigin: true,
    //   },
    // },
  },
});
