from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mysql+pymysql://root:@localhost:3306/databrew')

# Check monthly data
query = """
SELECT 
    DATE(transaction_date) as date, 
    SUM(transaction_qty * unit_price) as revenue, 
    COUNT(DISTINCT transaction_id) as orders,
    SUM(transaction_qty) as items_sold
FROM transactions 
WHERE transaction_date >= DATE_SUB('2025-11-30', INTERVAL 30 DAY) 
GROUP BY DATE(transaction_date) 
ORDER BY date DESC
"""

df = pd.read_sql(query, engine)
print("Daily Sales Data:")
print(df)
print("\n=== MONTHLY SUMMARY ===")
print(f"Total Revenue: ৳{df['revenue'].sum():,.2f}")
print(f"Total Orders: {df['orders'].sum()}")
print(f"Total Items Sold: {df['items_sold'].sum()}")
print(f"Avg Order Value: ৳{df['revenue'].sum() / df['orders'].sum():.2f}")

# Check average revenue
avg_revenue = df['revenue'].sum() / len(df)
print(f"\nAverage Daily Revenue: ৳{avg_revenue:,.2f}")
