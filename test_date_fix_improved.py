"""
Improved Playwright test for date selection fix - uses Streamlit-specific selectors
"""
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime

async def test_date_selection_streamlit():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()

        # Navigate to the application
        print("📍 Navigating to http://localhost:8514...")
        await page.goto("http://localhost:8514", wait_until="networkidle", timeout=60000)

        # Wait for initial load
        await asyncio.sleep(5)

        # Take initial screenshot
        await page.screenshot(path="/Users/michaeldurante/wzrd-algo/screenshots/streamlit_01_initial.png", full_page=True)
        print("✅ Screenshot 1: Initial state - showing date 2025/08/01")

        # Log the current visible text
        page_text = await page.locator('body').inner_text()
        if "2025-08-01" in page_text or "Live Strategy executed" in page_text:
            print("  ✓ Initial date detected in page content")

        # Test dates - we'll click and type into the date input
        test_dates = [
            ("08/02/2024", "Aug 2, 2024"),
            ("08/03/2024", "Aug 3, 2024"),
            ("08/05/2024", "Aug 5, 2024"),
            ("08/15/2024", "Aug 15, 2024"),
        ]

        screenshot_num = 2

        for date_value, date_label in test_dates:
            print(f"\n🔄 Testing date: {date_label} (entering {date_value})")

            try:
                # Find the date input - it's visible in the sidebar with value "2025/08/01"
                # Try multiple Streamlit-specific selectors
                date_inputs = [
                    'input[type="text"][value*="2025"]',  # Text input with 2025
                    'input[type="text"][value*="/"]',      # Text input with date format
                    'div[data-testid="stDateInput"] input', # Streamlit date input
                    'input[aria-label*="date"]',           # Input with date label
                ]

                date_input = None
                for selector in date_inputs:
                    elements = page.locator(selector)
                    count = await elements.count()
                    if count > 0:
                        date_input = elements.first
                        print(f"  Found date input using selector: {selector}")
                        break

                if date_input:
                    # Triple-click to select all text
                    await date_input.click(click_count=3)
                    await asyncio.sleep(0.3)

                    # Type new date
                    await date_input.fill(date_value)
                    await asyncio.sleep(0.3)

                    # Press Tab or Enter to trigger update
                    await date_input.press("Tab")
                    await asyncio.sleep(0.5)

                    # Look for "Reload Strategy & Data" button and click it
                    reload_button = page.locator('button:has-text("Reload Strategy & Data")')
                    if await reload_button.count() > 0:
                        print("  Clicking 'Reload Strategy & Data' button...")
                        await reload_button.click()
                        await asyncio.sleep(2)

                    # Wait for chart to update (look for success message)
                    print(f"  Waiting for strategy execution...")
                    await asyncio.sleep(8)

                    # Check for execution message
                    page_text = await page.locator('body').inner_text()
                    if "Live Strategy executed" in page_text:
                        print(f"  ✓ Strategy execution detected")

                        # Extract the date from the message
                        if date_value.replace("/", "-") in page_text or date_label in page_text:
                            print(f"  ✓ Correct date found in execution message!")
                        else:
                            print(f"  ⚠️  Date in execution message doesn't match")

                    # Take screenshot
                    screenshot_path = f"/Users/michaeldurante/wzrd-algo/screenshots/streamlit_{screenshot_num:02d}_date_{date_value.replace('/', '_')}.png"
                    await page.screenshot(path=screenshot_path, full_page=True)
                    print(f"✅ Screenshot {screenshot_num}: {date_label} captured")
                    screenshot_num += 1

                    # Scroll to charts area
                    charts_section = page.locator('text="Individual Trade Execution Analysis"')
                    if await charts_section.count() > 0:
                        await charts_section.scroll_into_view_if_needed()
                        await asyncio.sleep(1)

                        # Take chart closeup screenshot
                        chart_screenshot_path = f"/Users/michaeldurante/wzrd-algo/screenshots/streamlit_{screenshot_num:02d}_chart_{date_value.replace('/', '_')}.png"
                        await page.screenshot(path=chart_screenshot_path, full_page=True)
                        print(f"✅ Screenshot {screenshot_num}: Chart view for {date_label}")
                        screenshot_num += 1

                    # Scroll back to top
                    await page.locator('body').scroll_into_view_if_needed()
                    await asyncio.sleep(0.5)

                else:
                    print(f"  ❌ Could not find date input field with any selector")

            except Exception as e:
                print(f"  ❌ Error testing date {date_label}: {str(e)}")
                # Take error screenshot
                error_screenshot_path = f"/Users/michaeldurante/wzrd-algo/screenshots/error_{screenshot_num:02d}.png"
                await page.screenshot(path=error_screenshot_path, full_page=True)
                screenshot_num += 1

        # Test "Complete Overview" chart option
        print("\n🔄 Testing 'Complete Overview' chart option...")
        try:
            complete_overview = page.locator('text="Complete Overview"')
            if await complete_overview.count() > 0:
                # Look for the radio button or checkbox
                radio = page.locator('input[type="radio"][value="Complete Overview"], input[type="checkbox"] + label:has-text("Complete Overview")')
                if await radio.count() > 0:
                    await radio.first.click()
                    await asyncio.sleep(3)

                    screenshot_path = f"/Users/michaeldurante/wzrd-algo/screenshots/streamlit_{screenshot_num:02d}_complete_overview.png"
                    await page.screenshot(path=screenshot_path, full_page=True)
                    print(f"✅ Screenshot {screenshot_num}: Complete Overview mode")
                    screenshot_num += 1

        except Exception as e:
            print(f"  ℹ️  Could not switch to Complete Overview: {str(e)}")

        # Final summary screenshot
        await asyncio.sleep(2)
        await page.screenshot(path=f"/Users/michaeldurante/wzrd-algo/screenshots/streamlit_{screenshot_num:02d}_final.png", full_page=True)
        print(f"\n✅ Screenshot {screenshot_num}: Final state captured")

        print("\n" + "="*70)
        print("📊 TEST SUMMARY")
        print("="*70)
        print(f"Total screenshots captured: {screenshot_num}")
        print(f"Screenshots location: /Users/michaeldurante/wzrd-algo/screenshots/")
        print("\n📝 OBSERVATIONS TO CHECK:")
        print("1. Each date change should show the SELECTED date, not 150 days prior")
        print("2. Look for '🏗️ CHART FIX' debug messages in terminal/logs")
        print("3. Chart X-axis should show the correct date range")
        print("4. 'Live Strategy executed' message should show correct date")
        print("5. Both individual and overview charts should match selected date")
        print("="*70)

        # Keep browser open for inspection
        print("\n⏸️  Browser will remain open for 30 seconds for manual inspection...")
        await asyncio.sleep(30)

        await browser.close()

if __name__ == "__main__":
    print("🚀 Starting Streamlit-specific date selection test...")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    import os
    os.makedirs("/Users/michaeldurante/wzrd-algo/screenshots", exist_ok=True)

    asyncio.run(test_date_selection_streamlit())
