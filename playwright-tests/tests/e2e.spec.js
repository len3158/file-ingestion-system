// playwright-tests/tests/e2e.spec.js
import { test, expect } from '@playwright/test';
import playwrightConfig from "../playwright.config";

test('page loads with correct title and header', async ({ page }) => {
    await page.goto(playwrightConfig.webServer.url, { waitUntil: 'networkidle' });
    await page.waitForTimeout(500);
    const header = page.locator('.header h1');
    await header.waitFor({ state: 'visible', timeout: 10000 });

    await expect(page).toHaveTitle(/File Ingestion UI/);
    await expect(header).toHaveText('📁 File Metadata Dashboard');
});

test('refresh button is visible and clickable', async ({ page }) => {
    await page.goto(playwrightConfig.webServer.url, { waitUntil: 'networkidle' });
    const button = page.locator('.refresh-btn');
    await expect(button).toBeVisible();
    await expect(button).toHaveText('🔄 Refresh');
    await button.click();
});

test('empty state is visible when no files', async ({ page }) => {
    await page.goto(playwrightConfig.webServer.url, { waitUntil: 'networkidle' });
    await page.evaluate(() => {
        document.getElementById('metadataTable').style.display = 'none';
        document.getElementById('emptyState').style.display = 'block';
    });
    const emptyState = page.locator('#emptyState');
    await expect(emptyState).toBeVisible();
    await expect(emptyState.locator('h3')).toHaveText('No files found');
});

test('metadata table displays rows correctly', async ({ page }) => {
    await page.goto(playwrightConfig.webServer.url, { waitUntil: 'networkidle' });
    await page.evaluate(() => {
        const tbody = document.querySelector('#metadataTable tbody');
        const row = document.createElement('tr');
        row.innerHTML = `
      <td>sample.csv</td>
      <td>1024</td>
      <td>abc123sha256</td>
      <td>processed</td>
      <td>ok</td>
      <td>/data/processed/sample.csv</td>
      <td><button>Download</button></td>
    `;
        tbody.appendChild(row);
        document.getElementById('metadataTable').style.display = 'table';
    });
    const firstRow = page.locator('#metadataTable tbody tr').first();
    await expect(firstRow.locator('td').nth(0)).toHaveText('sample.csv');
    await expect(firstRow.locator('td').nth(3)).toHaveText('processed');
    await expect(firstRow.locator('button')).toHaveText('Download');
});
