# Data extracted from the user's image
# Underlying: GOOG
# Price: 290.08
# Expiry: Jun 18, 2026

underlying_price = 290.08

data = [
    {"strike": 175, "ask": 121.65},
    {"strike": 180, "ask": 118.00},
    {"strike": 185, "ask": 112.05},
    {"strike": 190, "ask": 107.60},
    {"strike": 195, "ask": 103.20},
    {"strike": 200, "ask": 98.90},
    {"strike": 205, "ask": 94.65},
    {"strike": 210, "ask": 90.35},
    {"strike": 215, "ask": 86.25},
    {"strike": 220, "ask": 82.30},
    {"strike": 225, "ask": 78.30},
    {"strike": 230, "ask": 74.40},
    {"strike": 235, "ask": 70.75},
    {"strike": 240, "ask": 67.05},
    {"strike": 245, "ask": 63.55},
    {"strike": 250, "ask": 60.10},
    {"strike": 255, "ask": 56.90},
    {"strike": 260, "ask": 53.70},
    {"strike": 265, "ask": 50.55},
    {"strike": 270, "ask": 47.60},
    {"strike": 275, "ask": 44.80},
    {"strike": 280, "ask": 42.05},
    {"strike": 285, "ask": 39.45}
]

print(f"Underlying Price: {underlying_price}")
print("-" * 90)
print(f"{'Strike':<10} {'Ask':<10} {'Intrinsic':<10} {'TimeVal':<10} {'Lev(Cap)':<10} {'BreakEven%':<12}")
print("-" * 90)

closest_2x = None
min_diff_2x = float('inf')
lowest_time_value = None
min_time_value = float('inf')

for row in data:
    strike = row['strike']
    ask = row['ask']
    
    intrinsic_value = max(0, underlying_price - strike)
    time_value = ask - intrinsic_value
    capital_leverage = underlying_price / ask
    break_even_pct = ((strike + ask - underlying_price) / underlying_price) * 100
    
    row['intrinsic_value'] = intrinsic_value
    row['time_value'] = time_value
    row['capital_leverage'] = capital_leverage
    row['break_even_pct'] = break_even_pct
    
    print(f"{strike:<10.2f} {ask:<10.2f} {intrinsic_value:<10.2f} {time_value:<10.2f} {capital_leverage:<10.2f} {break_even_pct:<12.2f}%")
    
    # Track closest to 2x
    diff_2x = abs(capital_leverage - 2)
    if diff_2x < min_diff_2x:
        min_diff_2x = diff_2x
        closest_2x = row
        
    # Track lowest time value
    if time_value < min_time_value:
        min_time_value = time_value
        lowest_time_value = row

print("-" * 90)
print("Analysis:")
if closest_2x:
    print(f"\nClosest to 2x Capital Leverage:\nStrike: {closest_2x['strike']}, Ask: {closest_2x['ask']}, Lev: {closest_2x['capital_leverage']:.2f}, TimeVal: {closest_2x['time_value']:.2f}")

if lowest_time_value:
    print(f"\nLowest Time Value (Cheapest financing):\nStrike: {lowest_time_value['strike']}, Ask: {lowest_time_value['ask']}, Lev: {lowest_time_value['capital_leverage']:.2f}, TimeVal: {lowest_time_value['time_value']:.2f}")
