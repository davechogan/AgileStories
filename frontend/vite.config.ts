import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@ai': fileURLToPath(new URL('../ai', import.meta.url)),
      '@scripts': fileURLToPath(new URL('../scripts', import.meta.url))
    }
  }
}) 