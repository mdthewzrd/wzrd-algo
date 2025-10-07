const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  const page = await context.newPage();

  // Enable console logging from the page
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));

  try {
    console.log('Navigating to http://localhost:8514...');
    await page.goto('http://localhost:8514', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);

    console.log('\n=== INITIAL STATE ===');
    await page.screenshot({ path: '/Users/michaeldurante/wzrd-algo/step1_initial.png', fullPage: true });

    // Get the current date value from the input
    const dateInput = await page.locator('input[type="text"]').first();
    const currentValue = await dateInput.inputValue();
    console.log(`Current date input value: ${currentValue}`);

    // Look for the Strategy Chart tab and click it
    console.log('\n=== CLICKING STRATEGY CHART TAB ===');
    const strategyChartTab = await page.locator('text=Strategy Chart').first();
    if (await strategyChartTab.count() > 0) {
      await strategyChartTab.click();
      await page.waitForTimeout(2000);
      await page.screenshot({ path: '/Users/michaeldurante/wzrd-algo/step2_chart_view.png', fullPage: true });
      console.log('Clicked Strategy Chart tab');
    }

    // Try to find and read any text that shows dates on the chart
    const bodyText = await page.locator('body').innerText();

    // Look for date patterns in the page
    const datePattern = /\d{4}[-\/]\d{2}[-\/]\d{2}/g;
    const foundDates = bodyText.match(datePattern);
    console.log('\n=== DATES FOUND ON PAGE ===');
    if (foundDates) {
      foundDates.forEach(date => console.log(`  - ${date}`));
    }

    // Check what the loaded strategy file says
    console.log('\n=== CHECKING LOADED STRATEGY ===');
    const loadedText = await page.locator('text=/Loaded.*strategy/i').first().innerText().catch(() => 'Not found');
    console.log(`Loaded strategy: ${loadedText}`);

    // Check the status messages
    const statusMessages = await page.locator('text=/Generated.*signals for/i').all();
    for (const msg of statusMessages) {
      const text = await msg.innerText();
      console.log(`Status: ${text}`);
    }

    // Now let's try to change the date
    console.log('\n=== ATTEMPTING TO CHANGE DATE ===');

    // Click on the date input to open the date picker
    await dateInput.click();
    await page.waitForTimeout(1000);
    await page.screenshot({ path: '/Users/michaeldurante/wzrd-algo/step3_datepicker_open.png', fullPage: true });
    console.log('Opened date picker');

    // Try to select a different date (e.g., click on day 15)
    const day15 = await page.locator('button:has-text("15")').first();
    if (await day15.count() > 0 && await day15.isVisible()) {
      console.log('Clicking on day 15...');
      await day15.click();
      await page.waitForTimeout(2000);

      const newValue = await dateInput.inputValue();
      console.log(`New date input value: ${newValue}`);

      await page.screenshot({ path: '/Users/michaeldurante/wzrd-algo/step4_after_date_change.png', fullPage: true });

      // Check if there's a reload button and click it
      const reloadButton = await page.locator('text=Reload Strategy').first();
      if (await reloadButton.count() > 0) {
        console.log('Clicking reload button...');
        await reloadButton.click();
        await page.waitForTimeout(3000);
        await page.screenshot({ path: '/Users/michaeldurante/wzrd-algo/step5_after_reload.png', fullPage: true });

        // Check the new status messages
        const newStatusMessages = await page.locator('text=/Generated.*signals for/i').all();
        console.log('\n=== AFTER RELOAD ===');
        for (const msg of newStatusMessages) {
          const text = await msg.innerText();
          console.log(`Status: ${text}`);
        }
      }
    }

    // Check if we can access the JavaScript variables/state
    console.log('\n=== CHECKING JAVASCRIPT STATE ===');
    const jsState = await page.evaluate(() => {
      // Try to access any global variables that might hold the date
      return {
        windowKeys: Object.keys(window).filter(k => k.includes('date') || k.includes('Date') || k.includes('strategy')),
        localStorage: JSON.parse(JSON.stringify(localStorage)),
      };
    });
    console.log('Window keys with date/strategy:', jsState.windowKeys);
    console.log('LocalStorage:', JSON.stringify(jsState.localStorage, null, 2));

    console.log('\n=== Screenshots saved ===');
    console.log('1. step1_initial.png - Initial state');
    console.log('2. step2_chart_view.png - Chart view');
    console.log('3. step3_datepicker_open.png - Date picker opened');
    console.log('4. step4_after_date_change.png - After changing date');
    console.log('5. step5_after_reload.png - After reload');

    // Keep browser open for inspection
    console.log('\nBrowser will remain open for 30 seconds for manual inspection...');
    await page.waitForTimeout(30000);

  } catch (error) {
    console.error('Error:', error.message);
    console.error(error.stack);
    await page.screenshot({ path: '/Users/michaeldurante/wzrd-algo/error_screenshot.png' });
  } finally {
    await browser.close();
  }
})();
