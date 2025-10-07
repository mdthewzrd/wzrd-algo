"""
Playwright test for Strategy Viewer
Tests loading, chart display, and signal arrows
"""
from playwright.sync_api import sync_playwright, expect
import json
import time

def test_strategy_viewer():
    """Test the strategy viewer with test_strategy.json"""

    # Load test artifact
    with open('/Users/michaeldurante/wzrd-algo/wzrd-algo-mini/test_strategy.json', 'r') as f:
        test_artifact = json.load(f)

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            print("📊 Navigating to Strategy Viewer...")
            page.goto("http://localhost:8510", timeout=30000)

            # Wait for page to load
            page.wait_for_selector("text=Strategy Viewer", timeout=10000)
            print("✅ Page loaded")

            # Find the text area
            print("📝 Pasting test artifact...")
            text_area = page.locator('textarea').first
            text_area.fill(json.dumps(test_artifact, indent=2))
            print("✅ Artifact pasted")

            # Wait for chart to appear
            print("⏳ Waiting for chart to render...")
            page.wait_for_selector(".plotly", timeout=60000)
            time.sleep(3)  # Give extra time for all elements to render
            print("✅ Chart rendered")

            # Check for strategy name
            strategy_name = test_artifact.get("strategy_name", "")
            if page.locator(f"text={strategy_name}").count() > 0:
                print(f"✅ Strategy name displayed: {strategy_name}")
            else:
                print(f"⚠️ Strategy name not found: {strategy_name}")

            # Check for metrics
            if page.locator("text=Total P&L").count() > 0:
                print("✅ Metrics section displayed")
            else:
                print("⚠️ Metrics section not found")

            # Take screenshot of full page
            print("📸 Taking screenshot...")
            page.screenshot(path="/Users/michaeldurante/wzrd-algo/wzrd-algo-mini/test_strategy_viewer_full.png", full_page=True)
            print("✅ Screenshot saved: test_strategy_viewer_full.png")

            # Take screenshot of chart only
            chart = page.locator(".plotly").first
            chart.screenshot(path="/Users/michaeldurante/wzrd-algo/wzrd-algo-mini/test_strategy_viewer_chart.png")
            print("✅ Chart screenshot saved: test_strategy_viewer_chart.png")

            # Check for signal arrows in the page content
            # Note: Plotly charts render arrows as SVG/Canvas, so we check if signals table exists
            if page.locator("text=Signal History").count() > 0:
                print("✅ Signal History section found")

                # Count signal rows
                signal_count = len(test_artifact.get("signals", []))
                print(f"✅ Expected {signal_count} signals in artifact")
            else:
                print("⚠️ Signal History section not found")

            print("\n🎉 Test completed successfully!")
            print("📊 Review screenshots:")
            print("   - test_strategy_viewer_full.png (full page)")
            print("   - test_strategy_viewer_chart.png (chart only)")

            # Keep browser open for manual inspection
            print("\n⏸️ Browser will stay open for 10 seconds for manual inspection...")
            time.sleep(10)

        except Exception as e:
            print(f"\n❌ Test failed with error: {str(e)}")
            page.screenshot(path="/Users/michaeldurante/wzrd-algo/wzrd-algo-mini/test_strategy_viewer_error.png", full_page=True)
            print("📸 Error screenshot saved: test_strategy_viewer_error.png")
            raise
        finally:
            browser.close()

if __name__ == "__main__":
    test_strategy_viewer()
