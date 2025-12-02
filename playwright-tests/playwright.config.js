// playwright-tests/playwright.config.js
import { defineConfig } from '@playwright/test';

export default defineConfig({
    testDir: './tests',
    timeout: 60000,
    use: {
        headless: true,
        viewport: { width: 1280, height: 720 },
        ignoreHTTPSErrors: true,
        actionTimeout: 20000,
        navigationTimeout: 30000,
        slowMo: 100,
    },
    webServer: {
        command: 'npx serve -s ../ui -l 3000',
        url: 'http://localhost:3000',
        reuseExistingServer: true,
    },
});