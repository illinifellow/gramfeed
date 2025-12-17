import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// built into backend/static and served by FastAPI, so the admin needs no host of its own
export default defineConfig({ plugins: [react()], build: { outDir: "../backend/gramfeed/static", emptyOutDir: true }, base: "/admin/" });