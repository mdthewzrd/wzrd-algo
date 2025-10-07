# Manual Testing Instructions for Date Selection Fix

## Test Overview
Testing the fix for the date selection bug where charts were showing data from 150 days before the selected date instead of the actual selected date.

## Current Status from Automated Test

### ✅ What Worked:
1. Successfully navigated to http://localhost:8514
2. Located and interacted with the date input field
3. Changed dates to: Aug 3, Aug 5, and Aug 15, 2024
4. Clicked "Reload Strategy & Data" button successfully
5. Captured 6 screenshots showing the UI state

### ⚠️ Issues Observed:
1. **Date format confusion**: Date input shows format like "0803/20/24" instead of "08/03/2024"
2. **Execution message not updating**: Message still shows "2025-08-01" after date changes
3. **No debug output captured**: The "🏗️ CHART FIX" messages are in the code but not visible in test output

## Manual Testing Steps

### Step 1: Check Current State
1. Open browser to http://localhost:8514
2. Note the current date shown in the sidebar (should be in "Market Data Selection" section)
3. Note the "Live Strategy executed" message at the top
4. Screenshot the initial state

### Step 2: Change Date to Aug 2, 2024
1. Click on the date input field in the left sidebar
2. Change the date to **08/02/2024** (or try different format: 2024-08-02)
3. Click the red "Reload Strategy & Data" button
4. Wait for reload to complete (watch for success checkmark message)
5. **Verify the execution message shows the NEW date**
6. Scroll down to view the chart
7. **Check the X-axis labels** - they should show dates around Aug 2, 2024, NOT from March/April 2024

### Step 3: Monitor Terminal Logs
While changing dates, watch the terminal where Streamlit is running for these messages:

```
🏗️ CHART FIX: Target date 2024-08-02
🏗️ CHART FIX: Chart window <start> to <end>
🏗️ CHART FIX: Extended data: <N> bars (...)
🏗️ CHART FIX: Target date indices: <N> bars
🏗️ CHART FIX: Target starts at index <X>, dataset ends at <Y>
🏗️ CHART FIX: Need to show <N> bars from target date to end
```

These messages indicate the fix is working correctly.

### Step 4: Test Multiple Dates
Repeat Step 2 for these dates:
- Aug 3, 2024
- Aug 5, 2024
- Aug 15, 2024
- Sep 1, 2024

For EACH date:
- ✅ Check execution message shows correct date
- ✅ Check chart X-axis shows correct date range
- ✅ Check terminal logs show "🏗️ CHART FIX" messages
- ✅ Verify "Target date" in logs matches selected date

### Step 5: Test Both Chart Views
1. Look for radio buttons or checkboxes with:
   - "Individual Trade Executions" (default, selected)
   - "Complete Overview"

2. Click "Complete Overview"
3. **Verify the overview chart also shows the selected date**, not 150 days ago
4. Compare both chart views to ensure they're consistent

### Step 6: Calculate Expected Date Range

For a selected date (e.g., Aug 2, 2024):
- System loads 150 calendar days of data (for EMA calculation warmup)
- 150 days before Aug 2, 2024 = approximately March 4, 2024
- **OLD BUG**: Chart showed data from March 4, 2024 (the start of the 150-day window)
- **EXPECTED FIX**: Chart shows data from Aug 2, 2024 (the selected date)

The chart should show approximately:
- Start: Aug 2, 2024 at 9:30 AM
- End: Aug 2, 2024 at 4:00 PM (or later if extended hours)
- Approximately 78 bars for a full trading day (5-minute bars: 6.5 hours × 12 bars/hour)

## What to Look For

### ✅ Fix is Working If:
1. Execution message updates to show selected date
2. Chart X-axis labels show dates matching selected date
3. Terminal logs show "🏗️ CHART FIX" messages with correct dates
4. Both "Individual Trade Executions" and "Complete Overview" show same date
5. Debug output shows: "Need to show X bars from target date to end" (NOT "display_bars=150")

### ❌ Fix is NOT Working If:
1. Execution message shows old date (2025-08-01)
2. Chart X-axis shows dates from ~150 days ago (e.g., March when you selected August)
3. No "🏗️ CHART FIX" messages in terminal
4. Debug output shows: "display_bars=150" (old method)

## Screenshots Captured by Automated Test

1. `streamlit_01_initial.png` - Initial state (2025-08-01)
2. `streamlit_03_date_08_03_2024.png` - After changing to Aug 3
3. `streamlit_04_date_08_05_2024.png` - After changing to Aug 5
4. `streamlit_05_date_08_15_2024.png` - After changing to Aug 15
5. `streamlit_06_final.png` - Final state

## Terminal Log Location

The Streamlit app is running from:
- **Directory**: `/Users/michaeldurante/wzrd-algo/wzrd-algo-mini-clean`
- **File**: `apps/strategy_platform_complete.py`
- **PID**: 43815 (as of test time)

To view logs in real-time:
```bash
# Option 1: If logs are going to a file
tail -f /path/to/streamlit.log

# Option 2: Check the terminal where you started Streamlit
# (Look for the terminal window that shows Streamlit startup messages)
```

## Expected Debug Output Example

```
🏗️ CHART FIX: Target date 2024-08-05
🏗️ CHART FIX: Chart window 2024-08-05 09:30:00 to 2024-08-05 16:00:00
🏗️ CHART FIX: Extended data: 14892 bars (2024-03-07 09:30:00 to 2024-08-05 16:00:00)
🏗️ CHART FIX: Target date indices: 78 bars
🏗️ CHART FIX: Target starts at index 14814, dataset ends at 14891
🏗️ CHART FIX: Need to show 78 bars from target date to end
🏗️ CHART FIX: Target date range: 2024-08-05 09:30:00 to 2024-08-05 16:00:00
```

## Next Steps After Manual Testing

1. **If fix is working**: Document the verification and close the issue
2. **If fix is NOT working**:
   - Capture exact error messages
   - Note which dates fail
   - Check if the wrong file is being run
   - Verify the chart creation code is using the new `display_bars` calculation

## Questions to Answer

1. Does the date input accept the format properly?
2. Does clicking "Reload" actually reload with the new date?
3. Do the terminal logs show the debug messages?
4. Do the charts display the correct date range?
5. Is the data from the Polygon API for the correct date?
