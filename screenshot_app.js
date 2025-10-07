const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  const page = await context.newPage();

  try {
    console.log('Navigating to http://localhost:8514...');
    await page.goto('http://localhost:8514', { waitUntil: 'networkidle', timeout: 30000 });

    // Wait a bit for any dynamic content to load
    await page.waitForTimeout(2000);

    console.log('Taking initial screenshot...');
    await page.screenshot({ path: '/Users/michaeldurante/wzrd-algo/screenshot_initial.png', fullPage: true });

    // Try to find date inputs in the sidebar
    console.log('Looking for date selection controls...');
    const dateInputs = await page.locator('input[type="date"], input[type="datetime-local"], .date-picker').all();
    console.log(`Found ${dateInputs.length} date input elements`);

    // Get current visible text on the page for analysis
    const bodyText = await page.locator('body').innerText();
    console.log('Page loaded successfully');
    console.log('='.repeat(80));
    console.log('VISIBLE TEXT SAMPLE (first 500 chars):');
    console.log(bodyText.substring(0, 500));
    console.log('='.repeat(80));

    // Take a focused screenshot of the sidebar if it exists
    const sidebar = await page.locator('.sidebar, [class*="sidebar"], aside, [class*="panel"]').first();
    if (await sidebar.count() > 0) {
      console.log('Taking sidebar screenshot...');
      await sidebar.screenshot({ path: '/Users/michaeldurante/wzrd-algo/screenshot_sidebar.png' });
    }

    // Look for any visible charts
    const charts = await page.locator('canvas, svg[class*="chart"], [class*="chart"]').all();
    console.log(`Found ${charts.length} potential chart elements`);

    if (charts.length > 0) {
      console.log('Taking chart screenshot...');
      await charts[0].screenshot({ path: '/Users/michaeldurante/wzrd-algo/screenshot_chart.png' });
    }

    // Get the HTML structure of date-related elements
    const dateElements = await page.locator('input[type="date"], input[type="datetime-local"], label:has-text("date"), label:has-text("Date")').all();
    for (let i = 0; i < dateElements.length; i++) {
      const element = dateElements[i];
      const value = await element.getAttribute('value').catch(() => null);
      const text = await element.innerText().catch(() => null);
      const tagName = await element.evaluate(el => el.tagName);
      console.log(`Date element ${i}: ${tagName}, value: ${value}, text: ${text}`);
    }

    console.log('\nScreenshots saved:');
    console.log('- /Users/michaeldurante/wzrd-algo/screenshot_initial.png');
    console.log('- /Users/michaeldurante/wzrd-algo/screenshot_sidebar.png (if sidebar found)');
    console.log('- /Users/michaeldurante/wzrd-algo/screenshot_chart.png (if chart found)');

    // Keep browser open for 10 seconds to allow manual inspection
    console.log('\nBrowser will remain open for 10 seconds for manual inspection...');
    await page.waitForTimeout(10000);

  } catch (error) {
    console.error('Error:', error.message);
    await page.screenshot({ path: '/Users/michaeldurante/wzrd-algo/screenshot_error.png' });
  } finally {
    await browser.close();
  }
})();
