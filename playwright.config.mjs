import { defineConfig } from '@playwright/test';

// Browser QA serves the actual assembled artifact under the GitHub project
// prefix. It needs no framework model, external account, or paid API.
export default defineConfig({
  testDir: './tests/browser',
  timeout: 60000,
  workers: 1,
  retries: 0,
  reporter: [['list']],
  outputDir: 'browser-results',
  use: { browserName: 'chromium', baseURL: 'http://127.0.0.1:4173/ml_ai_it/', viewport: { width: 1440, height: 1000 }, trace: 'retain-on-failure', screenshot: 'only-on-failure' },
  webServer: { command: 'python scripts/serve_site.py --port 4173', url: 'http://127.0.0.1:4173/ml_ai_it/', reuseExistingServer: !process.env.CI, timeout: 30000 }
});
