"""
Playwright test for Signal Codifier validation
Tests the complete workflow of JSON validation and signal generation
"""

import asyncio
import json
from playwright.async_api import async_playwright

async def test_signal_codifier():
    """Test Signal Codifier with valid strategy JSON"""

    # Load our test strategy
    with open('test_strategy_current_valid.json', 'r') as f:
        test_strategy = json.load(f)

    test_json = json.dumps(test_strategy, indent=2)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Show browser for debugging
        page = await browser.new_page()

        try:
            print("🔄 Navigating to Signal Codifier...")
            await page.goto("http://localhost:8502")

            # Wait for page to load
            await page.wait_for_selector("text=Signal Codifier", timeout=10000)
            print("✅ Signal Codifier loaded successfully")

            # Scroll down to find the input section
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight/2)")
            await page.wait_for_timeout(1000)

            # Look for the radio buttons with more flexible selectors
            try:
                # Try to find "Paste JSON" radio button
                paste_json_radio = page.locator('input[type="radio"]').filter(has_text="Paste JSON")
                if await paste_json_radio.count() == 0:
                    # Alternative: look for the label
                    paste_json_label = page.locator('text=Paste JSON')
                    if await paste_json_label.count() > 0:
                        await paste_json_label.click()
                        print("✅ Selected 'Paste JSON' option via label")
                    else:
                        print("ℹ️ Paste JSON option not found, assuming default")
                else:
                    await paste_json_radio.first.click()
                    print("✅ Selected 'Paste JSON' option via radio button")
            except Exception as e:
                print(f"ℹ️ Radio button interaction failed: {e}, continuing...")

            # Find and fill the text area
            try:
                # Try multiple selectors for textarea
                textarea = None
                selectors = [
                    'textarea[placeholder*="strategy JSON"]',
                    'textarea[placeholder*="JSON"]',
                    'textarea',
                    '[data-testid="stTextArea"] textarea'
                ]

                for selector in selectors:
                    textarea_elements = page.locator(selector)
                    if await textarea_elements.count() > 0:
                        textarea = textarea_elements.first
                        break

                if textarea:
                    await textarea.fill(test_json)
                    print("✅ Pasted strategy JSON")
                else:
                    print("❌ Could not find textarea element")
                    return False
            except Exception as e:
                print(f"❌ Failed to fill textarea: {e}")
                return False

            # Wait a moment for JSON validation
            await page.wait_for_timeout(1000)

            # Check for success message
            try:
                await page.wait_for_selector("text=✅ Valid JSON loaded!", timeout=5000)
                print("✅ JSON validation passed")
            except:
                print("❌ JSON validation failed - no success message found")
                # Take screenshot for debugging
                await page.screenshot(path="codifier_validation_error.png")

                # Look for error messages
                error_elements = await page.query_selector_all('.stAlert, .alert, [data-testid="stAlert"]')
                for element in error_elements:
                    error_text = await element.inner_text()
                    print(f"❌ Error found: {error_text}")

                return False

            # Check strategy summary metrics
            try:
                strategy_name = await page.text_content('text=SPY_Current_Test_Strategy_Valid_20251002')
                if strategy_name:
                    print("✅ Strategy name displayed correctly")
                else:
                    print("❌ Strategy name not found")
            except:
                print("❌ Strategy summary not displayed")

            # Scroll to generation section
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)

            # Click the generate button
            generate_button = page.locator('button:has-text("Generate Code-True Signals")')
            await generate_button.click()
            print("✅ Clicked Generate button")

            # Wait for generation to complete (this might take time)
            try:
                await page.wait_for_selector("text=Code-True Strategy Generated!", timeout=30000)
                print("✅ Signal generation completed successfully")

                # Check for generated signals
                signals_section = page.locator("text=Generated Signals")
                if await signals_section.count() > 0:
                    print("✅ Signals section found")

                    # Look for signal expandables
                    signal_expanders = page.locator('[data-testid="stExpander"]')
                    signal_count = await signal_expanders.count()
                    print(f"✅ Found {signal_count} signal expanders")

                    if signal_count > 0:
                        # Click first signal to expand
                        await signal_expanders.first.click()
                        await page.wait_for_timeout(500)
                        print("✅ Expanded first signal for inspection")
                else:
                    print("❌ No signals section found")

                # Check for download button
                download_button = page.locator('button:has-text("Download JSON")')
                if await download_button.count() > 0:
                    print("✅ Download JSON button available")
                else:
                    print("❌ Download JSON button not found")

                # Take screenshot of success
                await page.screenshot(path="codifier_success.png")
                print("✅ Screenshot saved: codifier_success.png")

                return True

            except Exception as e:
                print(f"❌ Signal generation failed or timed out: {e}")

                # Take screenshot for debugging
                await page.screenshot(path="codifier_generation_error.png")

                # Look for error messages
                error_elements = await page.query_selector_all('.stAlert, .alert, [data-testid="stAlert"]')
                for element in error_elements:
                    error_text = await element.inner_text()
                    print(f"❌ Generation error: {error_text}")

                return False

        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            await page.screenshot(path="codifier_test_error.png")
            return False

        finally:
            await browser.close()

async def main():
    print("🧪 Starting Signal Codifier Playwright Test")
    success = await test_signal_codifier()

    if success:
        print("\n🎉 Signal Codifier test PASSED!")
        print("✅ JSON validation works")
        print("✅ Signal generation works")
        print("✅ UI responds correctly")
    else:
        print("\n❌ Signal Codifier test FAILED!")
        print("Check screenshots for debugging:")
        print("- codifier_validation_error.png")
        print("- codifier_generation_error.png")
        print("- codifier_test_error.png")

    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)