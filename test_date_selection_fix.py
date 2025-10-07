"""
Playwright test script to verify the date selection bug fix in Wizard Algo Mini
"""
import asyncio
import time
from playwright.async_api import async_playwright
from datetime import datetime

async def test_date_selection():
    async with async_playwright() as p:
        # Launch browser in headed mode so we can see what's happening
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()

        # Navigate to the application
        print("📍 Navigating to http://localhost:8514...")
        await page.goto("http://localhost:8514", wait_until="networkidle", timeout=60000)

        # Take initial screenshot
        await page.screenshot(path="/Users/michaeldurante/wzrd-algo/screenshots/01_initial_state.png", full_page=True)
        print("✅ Screenshot 1: Initial state captured")

        # Wait for page to fully load
        await asyncio.sleep(3)

        # Test different dates
        test_dates = [
            ("2024-08-02", "Aug 2, 2024"),
            ("2024-08-03", "Aug 3, 2024"),
            ("2024-08-05", "Aug 5, 2024"),
            ("2024-08-15", "Aug 15, 2024"),
            ("2024-09-01", "Sep 1, 2024")
        ]

        screenshot_num = 2

        for date_value, date_label in test_dates:
            print(f"\n🔄 Testing date: {date_label}")

            try:
                # Look for date input field (Streamlit uses different selectors)
                # Try multiple strategies to find the date input

                # Strategy 1: Look for date_input by label text
                date_input = page.locator('input[type="date"]').first

                if await date_input.count() > 0:
                    print(f"  Found date input field")

                    # Clear and set new date
                    await date_input.click()
                    await asyncio.sleep(0.5)

                    # Clear the field
                    await date_input.press("Control+A")
                    await date_input.press("Backspace")
                    await asyncio.sleep(0.3)

                    # Type new date
                    await date_input.fill(date_value)
                    await asyncio.sleep(0.5)

                    # Press Enter to trigger the change
                    await date_input.press("Enter")
                    print(f"  Set date to: {date_value}")

                    # Wait for chart to update
                    print(f"  Waiting for chart to update...")
                    await asyncio.sleep(5)

                    # Take screenshot
                    screenshot_path = f"/Users/michaeldurante/wzrd-algo/screenshots/{screenshot_num:02d}_date_{date_value.replace('-', '_')}.png"
                    await page.screenshot(path=screenshot_path, full_page=True)
                    print(f"✅ Screenshot {screenshot_num}: {date_label} captured")
                    screenshot_num += 1

                    # Check for any visible error messages
                    error_elements = page.locator('[data-testid="stException"]')
                    if await error_elements.count() > 0:
                        print(f"  ⚠️  WARNING: Error messages detected on page")

                    # Look for chart elements
                    chart_elements = page.locator('iframe[title*="chart"], canvas')
                    chart_count = await chart_elements.count()
                    print(f"  Found {chart_count} chart elements")

                else:
                    print(f"  ❌ Could not find date input field")

            except Exception as e:
                print(f"  ❌ Error testing date {date_label}: {str(e)}")
                # Take error screenshot
                error_screenshot_path = f"/Users/michaeldurante/wzrd-algo/screenshots/error_{screenshot_num:02d}_{date_value.replace('-', '_')}.png"
                await page.screenshot(path=error_screenshot_path, full_page=True)
                screenshot_num += 1

        # Test date range mode
        print("\n🔄 Testing date range mode...")

        try:
            # Look for radio buttons or checkboxes for single date vs date range
            range_selector = page.locator('text=/.*date range.*/i').first

            if await range_selector.count() > 0:
                await range_selector.click()
                await asyncio.sleep(2)

                screenshot_path = f"/Users/michaeldurante/wzrd-algo/screenshots/{screenshot_num:02d}_date_range_mode.png"
                await page.screenshot(path=screenshot_path, full_page=True)
                print(f"✅ Screenshot {screenshot_num}: Date range mode captured")
                screenshot_num += 1
            else:
                print("  ℹ️  Could not find date range selector - may not be available")

        except Exception as e:
            print(f"  ❌ Error testing date range mode: {str(e)}")

        # Final summary screenshot
        await asyncio.sleep(2)
        await page.screenshot(path=f"/Users/michaeldurante/wzrd-algo/screenshots/{screenshot_num:02d}_final_state.png", full_page=True)
        print(f"\n✅ Screenshot {screenshot_num}: Final state captured")

        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        print(f"Total screenshots captured: {screenshot_num}")
        print(f"Screenshots location: /Users/michaeldurante/wzrd-algo/screenshots/")
        print("\n📝 MANUAL VERIFICATION STEPS:")
        print("1. Check screenshots for each date change")
        print("2. Verify chart shows SELECTED date, not 150 days ago")
        print("3. Check terminal logs for '🏗️ CHART FIX' debug messages")
        print("4. Compare 'Individual Trade Executions' vs 'Complete Overview' charts")
        print("5. Verify date labels on X-axis match selected date")
        print("="*60)

        # Keep browser open for manual inspection
        print("\n⏸️  Browser will remain open for 30 seconds for manual inspection...")
        await asyncio.sleep(30)

        await browser.close()

if __name__ == "__main__":
    print("🚀 Starting Playwright test for date selection fix...")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Create screenshots directory
    import os
    os.makedirs("/Users/michaeldurante/wzrd-algo/screenshots", exist_ok=True)

    asyncio.run(test_date_selection())
