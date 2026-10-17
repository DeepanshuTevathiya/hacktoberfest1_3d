import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Same-origin requests avoid CORS and stale environment-variable problems in local development.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8001',
        changeOrigin: true,
      },
    },
  },
});
