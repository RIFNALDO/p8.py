"""
Retail Sales Processor
Assignment: DataFrames and Filtering with Pandas
"""

import pandas as pd
import numpy as np

print("=" * 62)
print("       🛒 RETAIL SALES PROCESSOR — PANDAS DEEP DIVE")
print("=" * 62)

# ── STEP 1 — GENERATE DATASET ────────────────────────────────
np.random.seed(7)
categories = ["Electronics", "Clothing", "Groceries", "Books", "Sports"]
stores = ["Store_A", "Store_B", "Store_C", "Store_D"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

records = []
for _ in range(60):
    records.append({
        "Store": np.random.choice(stores),
        "Category": np.random.choice(categories),
        "Month": np.random.choice(months),
        "Units_Sold": int(np.random.randint(5, 120)),
        "Unit_Price": round(float(np.random.uniform(10, 500)), 2),
        "Discount": round(float(np.random.choice([0, 0, 0.05, 0.10, 0.15, 0.20])), 2)
    })

sales = pd.DataFrame(records)

print(f"\n📋 STEP 1 — RAW DATA SNAPSHOT")
print(f"  Shape   : {sales.shape[0]} rows × {sales.shape[1]} columns")
print(f"  Columns : {list(sales.columns)}")
print(f"\n  First 5 rows:")
print(sales.head().to_string(index=False))

# ── STEP 2 — ADD CALCULATED COLUMNS ──────────────────────────
print("\n🧮 STEP 2 — CALCULATING REVENUE")
print("-" * 50)

sales["Gross_Revenue"] = sales["Units_Sold"] * sales["Unit_Price"]
sales["Net_Revenue"] = (sales["Units_Sold"] * sales["Unit_Price"] * (1 - sales["Discount"])).round(2)
sales["Discount_Amt"] = (sales["Gross_Revenue"] - sales["Net_Revenue"]).round(2)

print(f"  Total Gross Revenue : ₹ {sales['Gross_Revenue'].sum():>12,.2f}")
print(f"  Total Discounts     : ₹ {sales['Discount_Amt'].sum():>12,.2f}")
print(f"  Total Net Revenue   : ₹ {sales['Net_Revenue'].sum():>12,.2f}")
print(f"  Avg Transaction     : ₹ {sales['Net_Revenue'].mean():>12,.2f}")

# ── STEP 3 — STORE PERFORMANCE & idxmax() ────────────────────
print("\n🏪 STEP 3 — STORE PERFORMANCE")
print("-" * 58)

store_stats = sales.groupby("Store").agg(
    Transactions=("Net_Revenue", "count"),
    Total_Revenue=("Net_Revenue", "sum"),
    Avg_Revenue=("Net_Revenue", "mean"),
    Total_Units=("Units_Sold", "sum")
).round(2)

store_stats = store_stats.sort_values("Total_Revenue", ascending=False)
store_stats["Rank"] = range(1, len(store_stats) + 1)

print(f"{'Store':<10} {'Txns':>6} {'Total Rev':>14} {'Avg Rev':>11} {'Units':>8} {'Rank':>5}")
print("  " + "-" * 56)
for store, row in store_stats.iterrows():
    print(f"{store:<10} {int(row['Transactions']):>6} "
          f"₹{row['Total_Revenue']:>12,.2f} "
          f"₹{row['Avg_Revenue']:>9,.2f} "
          f"{int(row['Total_Units']):>8} "
          f"  #{int(row['Rank'])}")

# Use idxmax() to identify the best performing store
best_store = store_stats["Total_Revenue"].idxmax()
print(f"\n  🏆 Best performing store: {best_store} (₹{store_stats.loc[best_store, 'Total_Revenue']:,.2f})")

# ── STEP 4 — CATEGORY ANALYSIS ───────────────────────────────
print("\n📦 STEP 4 — CATEGORY ANALYSIS")
print("-" * 58)

cat_stats = sales.groupby("Category").agg(
    Total_Revenue=("Net_Revenue", "sum"),
    Avg_Discount=("Discount", "mean"),
    Units_Sold=("Units_Sold", "sum")
).round(2)

cat_stats["Revenue_Share_%"] = (cat_stats["Total_Revenue"] / cat_stats["Total_Revenue"].sum() * 100).round(1)
cat_stats = cat_stats.sort_values("Total_Revenue", ascending=False)

print(f"{'Category':<14} {'Total Rev':>13} {'Rev Share':>10} {'Avg Disc':>9} {'Units':>7}")
print("  " + "-" * 56)
for cat, row in cat_stats.iterrows():
    bar = "█" * int(row["Revenue_Share_%"] / 2)
    print(f"{cat:<14} ₹{row['Total_Revenue']:>11,.2f} "
          f"{row['Revenue_Share_%']:>5.1f}%  "
          f"{row['Avg_Discount'] * 100:>5.1f}%  "
          f"{int(row['Units_Sold']):>7} {bar}")

# ── STEP 5 — DISCOUNT LABEL WITH apply() ─────────────────────
print("\n🔍 STEP 5 — DISCOUNT LABEL WITH apply()")
print("-" * 50)

def discount_label(d):
    if d == 0:
        return "No Discount"
    elif d <= 0.1:
        return "Low (≤10%)"
    else:
        return "High (>10%)"

sales["Discount_Label"] = sales["Discount"].apply(discount_label)
print(sales["Discount_Label"].value_counts())

# ── STEP 6 — EXPORT RESULTS TO CSV ───────────────────────────
print("\n💾 STEP 6 — EXPORTING RESULTS")
sales.to_csv("processed_sales.csv", index=False)
store_stats.to_csv("store_summary.csv")
cat_stats.to_csv("category_summary.csv")
print("  ✅ Saved: processed_sales.csv, store_summary.csv, category_summary.csv")

print("=" * 62)