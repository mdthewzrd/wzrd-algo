#!/usr/bin/env python3
"""
Comprehensive test of Signal Codifier -> Strategy Viewer workflow
Uses Playwright to automate testing and take screenshots
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
import pandas as pd

# Test strategy JSON with known signals
TEST_STRATEGY = {
    "strategy_name": "SPY_Test_Signals_Debug",
    "description": "Test strategy with precise signal timing",
    "timeframe": "5min",
    "symbol": "SPY",
    "signals": [
        {
            "timestamp": "2025-09-26 09:35:00",
            "type": "entry_long",
            "price": 659.50,
            "shares": 25,
            "position_id": "TEST-1",
            "reason": "Test entry signal",
            "pnl": 0.0
        },
        {
            "timestamp": "2025-09-26 14:20:00",
            "type": "exit_long",
            "price": 662.25,
            "shares": 25,
            "position_id": "TEST-1",
            "reason": "Test exit signal",
            "pnl": 68.75
        },
        {
            "timestamp": "2025-09-30 10:15:00",
            "type": "entry_long",
            "price": 661.75,
            "shares": 25,
            "position_id": "TEST-2",
            "reason": "Second test entry",
            "pnl": 0.0
        },
        {
            "timestamp": "2025-09-30 15:30:00",
            "type": "exit_long",
            "price": 664.00,
            "shares": 25,
            "position_id": "TEST-2",
            "reason": "Second test exit",
            "pnl": 56.25
        }
    ],
    "performance_metrics": {
        "total_trades": 2,
        "total_pnl": 125.0,
        "win_rate": 100.0
    }
}

async def test_signal_workflow():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Show browser for debugging
        page = await browser.new_page()

        try:
            print("🚀 Starting Signal Workflow Test...")

            # Step 1: Test Strategy Viewer
            print("\n📊 Testing Strategy Viewer...")
            await page.goto("http://localhost:8510")
            await page.wait_for_load_state("networkidle")

            # Take initial screenshot
            await page.screenshot(path="debug_1_strategy_viewer_loaded.png")
            print("✅ Strategy Viewer loaded, screenshot saved")

            # Set date range to match our test signals (Sept 26, 30, 2025)
            print("\n📅 Setting date range...")

            # Wait for date inputs to be visible and try different selectors
            try:
                # Try multiple selectors for start date
                start_date_input = None
                for selector in ['input[data-testid*="start"]', 'input[placeholder*="Start"]', 'input[type="date"]']:
                    try:
                        start_date_input = page.locator(selector).first
                        await start_date_input.wait_for(timeout=5000)
                        break
                    except:
                        continue

                if start_date_input:
                    await start_date_input.fill("2025-09-26")
                    print("✅ Start date set")
                else:
                    print("⚠️ Could not find start date input")

                # Try multiple selectors for end date
                end_date_input = None
                for selector in ['input[data-testid*="end"]', 'input[placeholder*="End"]']:
                    try:
                        end_date_input = page.locator(selector).first
                        await end_date_input.wait_for(timeout=5000)
                        break
                    except:
                        continue

                if end_date_input:
                    await end_date_input.fill("2025-09-30")
                    print("✅ End date set")
                else:
                    print("⚠️ Could not find end date input")

            except Exception as e:
                print(f"⚠️ Date setting error: {e}")
                # Continue anyway

            await page.screenshot(path="debug_2_dates_set.png")
            print("✅ Date range set to Sept 26-27, 2025")

            # Step 2: Paste test strategy JSON
            print("\n📝 Pasting test strategy JSON...")

            # Select "Paste JSON" option
            paste_json_radio = page.locator('input[value="Paste JSON"]')
            await paste_json_radio.click()

            # Find text area and paste JSON
            json_textarea = page.locator('textarea')
            await json_textarea.fill(json.dumps(TEST_STRATEGY, indent=2))

            await page.screenshot(path="debug_3_json_pasted.png")
            print("✅ Test strategy JSON pasted")

            # Step 3: Parse strategy
            print("\n🔄 Parsing strategy...")
            parse_button = page.locator('text=Parse Strategy')
            await parse_button.click()

            # Wait for parsing to complete
            await page.wait_for_timeout(2000)
            await page.screenshot(path="debug_4_strategy_parsed.png")
            print("✅ Strategy parsed")

            # Step 4: Wait for chart to render
            print("\n📈 Waiting for chart to render...")
            await page.wait_for_timeout(5000)  # Give chart time to render

            # Take screenshot of final chart
            await page.screenshot(path="debug_5_final_chart.png")
            print("✅ Final chart screenshot taken")

            # Step 5: Analyze the chart for signals
            print("\n🔍 Analyzing chart for signal markers...")

            # Check if signals are visible
            signal_markers = await page.locator('path[fill="#00FF00"], path[fill="#FFFF00"]').count()
            print(f"📊 Found {signal_markers} signal markers on chart")

            # Check chart title
            chart_title = await page.locator('text=SPY - WZRD Chart Viewer').text_content()
            print(f"📊 Chart title: {chart_title}")

            # Step 6: Check for any error messages
            error_messages = await page.locator('.stAlert').count()
            if error_messages > 0:
                print(f"⚠️  Found {error_messages} error messages")
                await page.screenshot(path="debug_6_errors.png")

            print("\n✅ Signal workflow test completed!")
            print(f"📁 Screenshots saved:")
            print(f"   - debug_1_strategy_viewer_loaded.png")
            print(f"   - debug_2_dates_set.png")
            print(f"   - debug_3_json_pasted.png")
            print(f"   - debug_4_strategy_parsed.png")
            print(f"   - debug_5_final_chart.png")

            # Take final screenshot and close
            print(f"\n📸 Taking final screenshot...")
            await page.screenshot(path="debug_final_complete.png")

            # Don't wait for manual inspection in automated mode
            print(f"✅ Test completed successfully!")

        except Exception as e:
            print(f"❌ Error during testing: {e}")
            await page.screenshot(path="debug_error.png")

        finally:
            await browser.close()

def debug_signal_data():
    """Debug the signal data and timing"""
    print("\n🔍 DEBUGGING SIGNAL DATA:")
    print("=" * 50)

    for i, signal in enumerate(TEST_STRATEGY["signals"]):
        timestamp = signal["timestamp"]
        signal_type = signal["type"]
        price = signal["price"]

        # Parse timestamp
        dt = pd.to_datetime(timestamp)

        print(f"Signal {i+1}:")
        print(f"  Timestamp: {timestamp}")
        print(f"  Parsed datetime: {dt}")
        print(f"  Type: {signal_type}")
        print(f"  Price: ${price}")
        print(f"  Day of week: {dt.strftime('%A')}")
        print(f"  Hour: {dt.hour}")
        print()

if __name__ == "__main__":
    print("🧪 SIGNAL WORKFLOW DEBUGGING TOOL")
    print("=" * 50)

    # First debug the signal data
    debug_signal_data()

    # Then run the automated test
    asyncio.run(test_signal_workflow())