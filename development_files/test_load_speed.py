"""
Quick load speed test for strategy viewer
"""
import time
import json
from strategy_viewer import fetch_market_data, create_strategy_chart, load_strategy_artifact

# Load test artifact
with open('test_strategy.json', 'r') as f:
    test_artifact = json.load(f)

print("🚀 Testing Strategy Viewer Load Speed\n")

# Test 1: Data fetch speed
print("1️⃣ Testing data fetch speed...")
start = time.time()
data = fetch_market_data(
    symbol=test_artifact['symbol'],
    timeframe=test_artifact['timeframe'],
    days_back=2
)
fetch_time = time.time() - start
print(f"   ✓ Data fetch: {fetch_time:.2f}s ({len(data)} bars)")

# Test 2: Chart creation speed
print("\n2️⃣ Testing chart creation speed...")
start = time.time()
fig = create_strategy_chart(test_artifact)
chart_time = time.time() - start
print(f"   ✓ Chart creation: {chart_time:.2f}s")

# Test 3: Total load time (simulating first load)
print("\n3️⃣ Testing total load time (cold)...")
# Clear cache
fetch_market_data.clear()
start = time.time()
fig = create_strategy_chart(test_artifact)
total_time = time.time() - start
print(f"   ✓ Total time: {total_time:.2f}s")

# Test 4: Cached load time
print("\n4️⃣ Testing cached load time...")
start = time.time()
fig = create_strategy_chart(test_artifact)
cached_time = time.time() - start
print(f"   ✓ Cached time: {cached_time:.2f}s")

# Summary
print("\n" + "="*50)
print("📊 PERFORMANCE SUMMARY")
print("="*50)
print(f"First load:  {total_time:.2f}s {'✅' if total_time < 5 else '❌ TOO SLOW'}")
print(f"Cached load: {cached_time:.2f}s {'✅' if cached_time < 1 else '⚠️ SLOW'}")
print(f"Data bars:   {len(data)} bars")

if total_time < 5:
    print("\n🎉 Performance target MET! (<5 seconds)")
else:
    print(f"\n⚠️ Performance target MISSED by {total_time - 5:.2f}s")
