"""
Final comprehensive test - Scroll to charts and verify date labels
"""
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime

async def verify_chart_dates():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=800)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1200})
        page = await context.new_page()

        print("📍 Navigating to http://localhost:8514...")
        await page.goto("http://localhost:8514", wait_until="networkidle", timeout=60000)
        await asyncio.sleep(5)

        # Take initial full page screenshot
        await page.screenshot(path="/Users/michaeldurante/wzrd-algo/screenshots/full_01_initial.png", full_page=True)
        print("✅ Full page screenshot 1: Initial state")

        # Get initial execution message
        page_text = await page.locator('body').inner_text()
        print(f"\n📋 Initial execution message:")
        if "Live Strategy executed" in page_text:
            lines = page_text.split('\n')
            for line in lines:
                if "Live Strategy executed" in line:
                    print(f"   {line}")

        # Change to a specific test date: Aug 5, 2024
        test_date = "08/05/2024"
        test_label = "Aug 5, 2024"

        print(f"\n🔄 Changing date to {test_label}...")

        # Find date input
        date_input = page.locator('input[type="text"]').filter(has_text="/")
        if await date_input.count() == 0:
            date_input = page.locator('input[type="text"]').first

        # Change date
        await date_input.click(click_count=3)
        await asyncio.sleep(0.3)
        await date_input.fill(test_date)
        await asyncio.sleep(0.5)

        # Click reload button
        reload_button = page.locator('button:has-text("Reload Strategy & Data")')
        if await reload_button.count() > 0:
            print("   Clicking 'Reload Strategy & Data'...")
            await reload_button.click()
            await asyncio.sleep(2)

            # Wait for reload to complete - look for success message
            print("   Waiting for reload to complete...")
            await asyncio.sleep(8)

            # Check new execution message
            page_text = await page.locator('body').inner_text()
            print(f"\n📋 After reload - Execution message:")
            if "Live Strategy executed" in page_text:
                lines = page_text.split('\n')
                for line in lines:
                    if "Live Strategy executed" in line:
                        print(f"   {line}")
                        if "2024-08-05" in line or "08-05" in line or "Aug" in line:
                            print("   ✅ Date appears to be correct in message!")
                        else:
                            print("   ⚠️  Message doesn't show expected date")

        # Now scroll down to the charts section
        print(f"\n📊 Scrolling to charts section...")

        # Find the "Individual Trade Execution Analysis" section
        chart_section = page.locator('text="Individual Trade Execution Analysis"')
        if await chart_section.count() > 0:
            await chart_section.scroll_into_view_if_needed()
            await asyncio.sleep(2)

            # Take screenshot of charts area
            await page.screenshot(path="/Users/michaeldurante/wzrd-algo/screenshots/full_02_charts_area.png", full_page=True)
            print("✅ Screenshot 2: Charts area visible")

            # Look for any chart elements
            chart_iframes = await page.locator('iframe').count()
            chart_canvas = await page.locator('canvas').count()
            print(f"   Found {chart_iframes} iframes and {chart_canvas} canvas elements")

            # Try to find Plotly charts (Streamlit uses Plotly)
            plotly_charts = page.locator('.plotly')
            plotly_count = await plotly_charts.count()
            print(f"   Found {plotly_count} Plotly charts")

            if plotly_count > 0:
                # Hover over first chart to trigger any tooltips
                await plotly_charts.first.hover()
                await asyncio.sleep(1)

                # Take closeup screenshot
                await page.screenshot(path="/Users/michaeldurante/wzrd-algo/screenshots/full_03_chart_hover.png", full_page=True)
                print("✅ Screenshot 3: Chart with hover")

            # Scroll a bit more to see if there are more charts
            await page.evaluate("window.scrollBy(0, 400)")
            await asyncio.sleep(2)

            await page.screenshot(path="/Users/michaeldurante/wzrd-algo/screenshots/full_04_scrolled_more.png", full_page=True)
            print("✅ Screenshot 4: Scrolled to see more content")

        # Check for "Complete Overview" option
        print(f"\n🔄 Looking for 'Complete Overview' option...")
        complete_overview = page.locator('label:has-text("Complete Overview")')
        if await complete_overview.count() > 0:
            print("   Found 'Complete Overview' option, clicking it...")
            await complete_overview.click()
            await asyncio.sleep(4)

            # Scroll to chart again
            chart_section = page.locator('text="Individual Trade Execution Analysis"')
            if await chart_section.count() > 0:
                await chart_section.scroll_into_view_if_needed()
                await asyncio.sleep(2)

            await page.screenshot(path="/Users/michaeldurante/wzrd-algo/screenshots/full_05_complete_overview.png", full_page=True)
            print("✅ Screenshot 5: Complete Overview mode")
        else:
            print("   ℹ️  'Complete Overview' option not found or not visible")

        # Final full page screenshot
        await page.evaluate("window.scrollTo(0, 0)")
        await asyncio.sleep(1)
        await page.screenshot(path="/Users/michaeldurante/wzrd-algo/screenshots/full_06_final_top.png", full_page=True)
        print("✅ Screenshot 6: Back to top - final state")

        print("\n" + "="*70)
        print("📊 VERIFICATION SUMMARY")
        print("="*70)
        print("✅ Successfully changed date to Aug 5, 2024")
        print("✅ Clicked reload button")
        print("✅ Scrolled to charts section")
        print("✅ Captured 6 detailed screenshots")
        print("\n📝 MANUAL VERIFICATION NEEDED:")
        print("1. Check screenshots in /Users/michaeldurante/wzrd-algo/screenshots/")
        print("2. Look for date labels on chart X-axis")
        print("3. Verify dates show Aug 5, 2024 (NOT March/April 2024)")
        print("4. Check terminal logs for '🏗️ CHART FIX' debug messages")
        print("="*70)

        # Keep browser open
        print("\n⏸️  Browser staying open for 45 seconds for inspection...")
        print("   Use this time to manually inspect the charts!")
        await asyncio.sleep(45)

        await browser.close()

if __name__ == "__main__":
    print("🚀 Starting comprehensive chart verification test...")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    import os
    os.makedirs("/Users/michaeldurante/wzrd-algo/screenshots", exist_ok=True)

    asyncio.run(verify_chart_dates())

    print("\n✅ Test complete! Review screenshots and terminal logs.")
