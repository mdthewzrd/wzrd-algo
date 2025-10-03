"""
Test WZRD Chart Rendering with Playwright
Verifies that both daily and hourly charts render without errors
"""
import asyncio
from playwright.async_api import async_playwright
import time

async def test_chart_rendering():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1400, 'height': 1200})
        page = await context.new_page()

        print("🚀 Testing WZRD Chart Application on http://localhost:8509")

        # Navigate to Streamlit app
        try:
            await page.goto('http://localhost:8509', wait_until='networkidle', timeout=30000)
            await page.wait_for_timeout(5000)  # Wait for Streamlit to initialize

            print("✅ Page loaded successfully")

            # Take initial screenshot
            await page.screenshot(path='/Users/michaeldurante/wzrd-algo/wzrd-algo-mini/test_daily_chart.png', full_page=True)
            print("📸 Screenshot saved: test_daily_chart.png")

            # Check for error messages
            error_elements = await page.locator('text=/Error|error/i').count()
            if error_elements > 0:
                errors = await page.locator('text=/Error|error/i').all_text_contents()
                print(f"⚠️  Found {error_elements} error messages:")
                for error in errors:
                    print(f"   - {error}")
            else:
                print("✅ No error messages found on daily chart")

            # Check if chart canvas exists (Plotly creates canvas elements)
            canvas_count = await page.locator('canvas').count()
            print(f"📊 Found {canvas_count} canvas elements (charts)")

            if canvas_count >= 2:
                print("✅ Both main chart and volume chart detected")
            else:
                print(f"❌ Expected 2+ canvas elements, found {canvas_count}")

            # Check for the chart title
            title_visible = await page.locator('text=SPY - WZRD Chart Viewer').count() > 0
            if title_visible:
                print("✅ Chart title found: 'SPY - WZRD Chart Viewer'")
            else:
                print("⚠️  Chart title not found")

            # Check for debug message showing data loaded
            debug_text = await page.locator('text=/Debug: Loaded \\d+ records/').count()
            if debug_text > 0:
                debug_content = await page.locator('text=/Debug: Loaded \\d+ records/').first.text_content()
                print(f"✅ {debug_content}")

            # Switch to hourly timeframe
            print("\n🔄 Switching to hourly timeframe...")
            await page.wait_for_timeout(2000)

            # Find and click the timeframe dropdown
            timeframe_select = page.locator('select').first
            await timeframe_select.select_option('hour')

            # Wait for chart to reload
            await page.wait_for_timeout(8000)  # Wait for API call and chart rendering

            print("✅ Switched to hourly timeframe")

            # Take hourly screenshot
            await page.screenshot(path='/Users/michaeldurante/wzrd-algo/wzrd-algo-mini/test_hourly_chart.png', full_page=True)
            print("📸 Screenshot saved: test_hourly_chart.png")

            # Check for errors in hourly view
            error_elements_hour = await page.locator('text=/Error|error/i').count()
            if error_elements_hour > 0:
                errors = await page.locator('text=/Error|error/i').all_text_contents()
                print(f"⚠️  Found {error_elements_hour} error messages in hourly view:")
                for error in errors:
                    print(f"   - {error}")
            else:
                print("✅ No error messages found on hourly chart")

            # Check canvas count again
            canvas_count_hour = await page.locator('canvas').count()
            print(f"📊 Found {canvas_count_hour} canvas elements in hourly view")

            if canvas_count_hour >= 2:
                print("✅ Both main chart and volume chart detected in hourly view")
            else:
                print(f"❌ Expected 2+ canvas elements, found {canvas_count_hour}")

            # Check for after-hours shading (look for grey rectangles in hourly view)
            # Plotly adds vrect shapes, but they're in the canvas, so we check if hourly loaded properly
            hourly_debug = await page.locator('text=/Debug: Loaded \\d+ records.*hour/').count()
            if hourly_debug > 0:
                debug_content = await page.locator('text=/Debug: Loaded \\d+ records/').first.text_content()
                print(f"✅ {debug_content}")
                print("✅ After-hours shading should be visible in hourly chart")

            print("\n" + "="*60)
            print("📊 CHART RENDERING TEST SUMMARY")
            print("="*60)
            print(f"Daily Chart: {'✅ PASS' if canvas_count >= 2 and error_elements == 0 else '❌ FAIL'}")
            print(f"Hourly Chart: {'✅ PASS' if canvas_count_hour >= 2 and error_elements_hour == 0 else '❌ FAIL'}")
            print("="*60)

        except Exception as e:
            print(f"❌ Test failed with error: {str(e)}")
            await page.screenshot(path='/Users/michaeldurante/wzrd-algo/wzrd-algo-mini/test_error.png', full_page=True)
            print("📸 Error screenshot saved: test_error.png")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_chart_rendering())