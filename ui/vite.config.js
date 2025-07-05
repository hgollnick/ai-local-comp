import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  // Load env file based on mode
  const env = loadEnv(mode, process.cwd(), '');
  const apiTarget = env.VITE_API_TARGET || 'http://localhost:8000';
  console.log('apiTarget:', apiTarget);
  return {
    plugins: [react()],
    server: {
      proxy: {
        '/config': {
          target: apiTarget,
          changeOrigin: true,
        },
        '/models': {
          target: apiTarget,
          changeOrigin: true,
        },
        '/ask': {
          target: apiTarget,
          changeOrigin: true,
        },
        '/pull_model': {
          target: apiTarget,
          changeOrigin: true,
        },
        '/logs': {
          target: apiTarget,
          changeOrigin: true,
        },
      },
    },
  };
});
