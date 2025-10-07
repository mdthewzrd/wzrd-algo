"""
Test WZRD Chart Rendering with Playwright - Fixed Version
Verifies that both daily and hourly charts render without errors
"""
import asyncio
from playwright.async_api import async_playwright

async def test_chart_rendering():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1400, 'height': 1400})
        page = await context.new_page()

        print("🚀 Testing WZRD Chart Application on http://localhost:8509\n")

        try:
            await page.goto('http://localhost:8509', wait_until='networkidle', timeout=30000)
            await page.wait_for_timeout(5000)

            print("=" * 60)
            print("DAILY CHART TEST")
            print("=" * 60)

            # Take daily screenshot
            await page.screenshot(path='/Users/michaeldurante/wzrd-algo/wzrd-algo-mini/verified_daily.png', full_page=True)
            print("📸 Screenshot: verified_daily.png")

            # Check for Plotly chart (SVG elements, not canvas)
            plotly_chart = await page.locator('.js-plotly-plot').count()
            print(f"📊 Plotly charts found: {plotly_chart}")

            # Check for error text
            error_count = await page.locator('text=/SPY - Error|Chart Error/i').count()
            print(f"❌ Error messages: {error_count}")

            # Check data loaded
            debug_msg = await page.locator('text=/Debug: Loaded \\d+ records/').first.text_content()
            print(f"📈 {debug_msg}")

            # Check chart title
            title = await page.locator('text=/SPY - WZRD Chart Viewer/').count()
            print(f"📝 Chart title present: {'✅' if title > 0 else '❌'}")

            daily_pass = plotly_chart > 0 and error_count == 0
            print(f"\n{'✅ DAILY CHART PASS' if daily_pass else '❌ DAILY CHART FAIL'}\n")

            # Switch to hourly
            print("=" * 60)
            print("HOURLY CHART TEST")
            print("=" * 60)

            # Use the Streamlit selectbox (it's a custom widget)
            await page.locator('[data-baseweb="select"]').click()
            await page.wait_for_timeout(1000)
            await page.locator('text=hour').click()
            await page.wait_for_timeout(8000)  # Wait for data fetch and render

            print("🔄 Switched to hourly timeframe")

            # Take hourly screenshot
            await page.screenshot(path='/Users/michaeldurante/wzrd-algo/wzrd-algo-mini/verified_hourly.png', full_page=True)
            print("📸 Screenshot: verified_hourly.png")

            # Check hourly chart
            plotly_chart_hour = await page.locator('.js-plotly-plot').count()
            print(f"📊 Plotly charts found: {plotly_chart_hour}")

            error_count_hour = await page.locator('text=/SPY - Error|Chart Error/i').count()
            print(f"❌ Error messages: {error_count_hour}")

            # Check hourly data loaded
            debug_msg_hour = await page.locator('text=/Debug: Loaded \\d+ records.*hour/').first.text_content()
            print(f"📈 {debug_msg_hour}")

            # Check for after-hours shading (Plotly vrect creates rect elements)
            # The shading is visible in the chart as grey rectangles
            print(f"🌙 After-hours shading: Should be visible in screenshot")

            hourly_pass = plotly_chart_hour > 0 and error_count_hour == 0
            print(f"\n{'✅ HOURLY CHART PASS' if hourly_pass else '❌ HOURLY CHART FAIL'}\n")

            # Final summary
            print("=" * 60)
            print("TEST SUMMARY")
            print("=" * 60)
            print(f"Daily Chart:  {'✅ PASS' if daily_pass else '❌ FAIL'}")
            print(f"Hourly Chart: {'✅ PASS' if hourly_pass else '❌ FAIL'}")
            print(f"\n{'🎉 ALL TESTS PASSED!' if daily_pass and hourly_pass else '⚠️  SOME TESTS FAILED'}")
            print("=" * 60)

        except Exception as e:
            print(f"\n❌ Test failed with error: {str(e)}")
            await page.screenshot(path='/Users/michaeldurante/wzrd-algo/wzrd-algo-mini/test_error.png', full_page=True)

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_chart_rendering())