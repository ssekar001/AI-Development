import pandas as pd

# Create sample sales data
data = {
    "OrderID": [1001, 1002, 1003, 1004, 1005, 1006, 1007],
    "OrderDate": ["2025-08-30"] * 7,
    "CustomerID": ["CUST001", "CUST002", "CUST003", "CUST001", "CUST004", "CUST005", "CUST006"],
    "ProductID": ["PROD001", "PROD003", "PROD002", "PROD005", "PROD004", "PROD006", "PROD001"],
    "ProductName": ["Wireless Mouse", "Running Shoes", "USB-C Charger", "Yoga Mat", "Office Chair", "Blender", "Wireless Mouse"],
    "Category": ["Electronics", "Sportswear", "Electronics", "Fitness", "Furniture", "Kitchen", "Electronics"],
    "Quantity": [2, 1, 3, 1, 1, 2, 1],
    "UnitPrice": [25.99, 75.50, 18.00, 20.00, 120.00, 45.00, 25.99],
    "TotalPrice": [51.98, 75.50, 54.00, 20.00, 120.00, 90.00, 25.99],
    "SalesChannel": ["Website", "Amazon", "Shopify", "Website", "Amazon", "Website", "Shopify"]
}

df = pd.DataFrame(data)

# Save to CSV
df.to_csv("daily_sales_data.csv", index=False)

print("CSV file 'daily_sales_data.csv' has been created.")
