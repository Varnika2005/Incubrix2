import { test, expect } from '@playwright/test';

test.describe('IncuBrix AEO / SEO / GEO Visibility Engine E2E Browser Suite', () => {
  test('renders Overview dashboard with real SQLite metrics and navigates across all 9 modules', async ({
    page,
  }) => {
    await page.goto('/', { waitUntil: 'domcontentloaded' });

    // 1. Overview Section
    await expect(page.getByTestId('overview-section')).toBeVisible();
    await expect(page.getByTestId('kpi-questions-validated')).toHaveText('100');
    await expect(page.getByTestId('kpi-issues-total')).toHaveText('22');
    await expect(page.getByTestId('kpi-content-pages')).toHaveText('10');
    await expect(page.getByTestId('kpi-citations-total')).toHaveText('30');
    await expect(page.getByText('DEMO Records Strictly Excluded from Totals')).toBeVisible();

    // 2. Navigate to Visibility Tracker
    await page.getByTestId('nav-visibility').click();
    await expect(page.getByTestId('visibility-section')).toBeVisible();
    await expect(page.getByText('Multi-Market Search & AI Assistant Visibility Tracker')).toBeVisible();
    await expect(page.getByText('Two-Date Observation Comparison')).toBeVisible();

    // 3. Navigate to Technical SEO Audit
    await page.getByTestId('nav-audit').click();
    await expect(page.getByTestId('audit-section')).toBeVisible();
    await expect(page.getByText('ISS-001').first()).toBeVisible();
    await expect(
      page.getByText('Zero JSON-LD Structured Data (Organization & WebSite) on Homepage').first()
    ).toBeVisible();

    // Test interactive JSON-LD validator in Audit view
    await page.getByRole('button', { name: 'Validate JSON-LD' }).click();
    await expect(
      page.getByText('PASS: Valid schema.org JSON-LD structure with zero fabricated rating/review fields.')
    ).toBeVisible();

    // 4. Navigate to Content Studio
    await page.getByTestId('nav-content').click();
    await expect(page.getByTestId('content-section')).toBeVisible();
    await expect(page.getByText('PAGE-001').first()).toBeVisible();
    await page.getByRole('button', { name: 'Generate Brief' }).click();
    await expect(page.getByText('2-Sentence Direct Answer Draft:')).toBeVisible();

    // 5. Navigate to Citation Opportunities
    await page.getByTestId('nav-citations').click();
    await expect(page.getByTestId('citations-section')).toBeVisible();
    await expect(page.getByText('CIT-001').first()).toBeVisible();

    // 6. Navigate to Research Questions
    await page.getByTestId('nav-questions').click();
    await expect(page.getByTestId('questions-section')).toBeVisible();
    await expect(page.getByText('Q-001').first()).toBeVisible();

    // 7. Navigate to Reports
    await page.getByTestId('nav-reports').click();
    await expect(page.getByTestId('reports-section')).toBeVisible();
    await expect(page.getByText('Official Assessment Workbook Export Verification')).toBeVisible();

    // 8. Navigate to Launch Plan
    await page.getByTestId('nav-launch').click();
    await expect(page.getByTestId('launch-section')).toBeVisible();
    await expect(page.getByText('Week 1 (LP-W01)')).toBeVisible();

    // 9. Navigate to Settings & Data Sources
    await page.getByTestId('nav-settings').click();
    await expect(page.getByTestId('settings-section')).toBeVisible();
    await expect(page.getByText('Search & AI Assistant Provider Adapters (5 Integrations)')).toBeVisible();
  });
});
