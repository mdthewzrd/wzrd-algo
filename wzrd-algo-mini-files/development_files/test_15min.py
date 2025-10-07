"""
Test WZRD Chart - Verify 15min Timeframe with All Indicators
"""
import asyncio
from playwright.async_api import async_playwright

async def test_15min_chart():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1400, 'height': 1400})
        page = await context.new_page()

        print("🚀 Testing 15-Minute Chart on http://localhost:8509\n")

        try:
            await page.goto('http://localhost:8509', wait_until='networkidle', timeout=30000)
            await page.wait_for_timeout(5000)

            print("=" * 60)
            print("15-MINUTE CHART TEST")
            print("=" * 60)

            # Switch to 15min
            await page.locator('[data-baseweb="select"]').click()
            await page.wait_for_timeout(1000)
            await page.locator('text=15min').click()
            await page.wait_for_timeout(8000)  # Wait for data fetch and render

            print("🔄 Switched to 15min timeframe")

            # Take screenshot
            await page.screenshot(path='/Users/michaeldurante/wzrd-algo/wzrd-algo-mini/test_15min.png', full_page=True)
            print("📸 Screenshot: test_15min.png")

            # Check for Plotly chart
            plotly_chart = await page.locator('.js-plotly-plot').count()
            print(f"📊 Plotly charts found: {plotly_chart}")

            # Check for error text
            error_count = await page.locator('text=/SPY - Error|Chart Error/i').count()
            print(f"❌ Error messages: {error_count}")

            # Check data loaded
            debug_msg = await page.locator('text=/Debug: Loaded \\d+ records.*15min/').first.text_content()
            print(f"📈 {debug_msg}")

            # Check for indicators (all should be available for 15min)
            vwap_checkbox = await page.locator('text=VWAP').count()
            prev_close_checkbox = await page.locator('text=Prev Close').count()
            bands_920_checkbox = await page.locator('text=9/20 Bands').count()
            cloud_920_checkbox = await page.locator('text=9/20 Cloud').count()
            bands_7289_checkbox = await page.locator('text=72/89 Bands').count()
            cloud_7289_checkbox = await page.locator('text=72/89 Cloud').count()

            print(f"\n📊 Indicator Checkboxes:")
            print(f"  VWAP: {'✅' if vwap_checkbox > 0 else '❌'}")
            print(f"  Prev Close: {'✅' if prev_close_checkbox > 0 else '❌'}")
            print(f"  9/20 Bands: {'✅' if bands_920_checkbox > 0 else '❌'}")
            print(f"  9/20 Cloud: {'✅' if cloud_920_checkbox > 0 else '❌'}")
            print(f"  72/89 Bands: {'✅' if bands_7289_checkbox > 0 else '❌'}")
            print(f"  72/89 Cloud: {'✅' if cloud_7289_checkbox > 0 else '❌'}")

            # Test passes if chart loads, no errors, and all indicators are available
            test_pass = (
                plotly_chart > 0 and
                error_count == 0 and
                vwap_checkbox > 0 and
                prev_close_checkbox > 0 and
                bands_920_checkbox > 0 and
                cloud_920_checkbox > 0 and
                bands_7289_checkbox > 0 and
                cloud_7289_checkbox > 0
            )

            print(f"\n{'✅ 15-MINUTE CHART TEST PASSED!' if test_pass else '❌ 15-MINUTE CHART TEST FAILED'}")
            print("=" * 60)

        except Exception as e:
            print(f"\n❌ Test failed with error: {str(e)}")
            await page.screenshot(path='/Users/michaeldurante/wzrd-algo/wzrd-algo-mini/test_15min_error.png', full_page=True)

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_15min_chart())
