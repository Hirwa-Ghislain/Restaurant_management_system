import requests
import pandas as pd
import numpy as np
from datetime import datetime

try:
    # Fetch data for orders (similar to your task fetch)
    get_orders = requests.get("http://127.0.0.1:8000/orders/?user_id=1")
    get_orders.raise_for_status()
    orders = get_orders.json()  # Fetching order data
    print("Fetched orders:", orders[:5])  # Show the first few rows for brevity

    # Fetch data for reservations
    get_reservations = requests.get("http://127.0.0.1:8000/reservations/?user_id=1")
    get_reservations.raise_for_status()
    reservations = get_reservations.json()  # Fetching reservation data
    print("Fetched reservations:", reservations[:5])  # Show the first few rows for brevity

    # Create DataFrames from the fetched data
    orders_df = pd.DataFrame(orders)
    reservations_df = pd.DataFrame(reservations)

    # Q1: Augment data to create 500,000 rows for both datasets
    while len(orders_df) < 500000:
        orders_df = pd.concat([orders_df, orders_df], ignore_index=True)
    orders_df = orders_df.iloc[:500000]  # Ensure exact 500,000 rows
    print(f"Orders DataFrame now has {len(orders_df)} rows.")

    while len(reservations_df) < 500000:
        reservations_df = pd.concat([reservations_df, reservations_df], ignore_index=True)
    reservations_df = reservations_df.iloc[:500000]  # Ensure exact 500,000 rows
    print(f"Reservations DataFrame now has {len(reservations_df)} rows.")

    # Save to CSV files
    orders_df.to_csv("orders_data.csv", index=False)
    reservations_df.to_csv("reservations_data.csv", index=False)
    print("The DataFrames have been saved to 'orders_data.csv' and 'reservations_data.csv'.")

    # Q2: Describe the datasets
    print("\nOrders Dataset Description:")
    print(orders_df.describe(include='all'))

    print("\nReservations Dataset Description:")
    print(reservations_df.describe(include='all'))

    # Q3: Handle null values in both datasets
    print("\nChecking for null values in orders dataset...")
    print(orders_df.isnull().sum())
    orders_df.fillna("Unknown", inplace=True)  # Replace nulls with "Unknown" or a suitable value
    print("Null values replaced in orders.")

    print("\nChecking for null values in reservations dataset...")
    print(reservations_df.isnull().sum())
    reservations_df.fillna("Unknown", inplace=True)  # Replace nulls with "Unknown" or a suitable value
    print("Null values replaced in reservations.")

    # Q4: Perform basic data preprocessing
    # Example preprocessing steps:
    # - Convert dates to datetime format
    if 'order_date' in orders_df.columns:
        orders_df['order_date'] = pd.to_datetime(orders_df['order_date'], errors='coerce')
    if 'delivery_date' in orders_df.columns:
        orders_df['delivery_date'] = pd.to_datetime(orders_df['delivery_date'], errors='coerce')
    
    if 'reservation_time' in reservations_df.columns:
        reservations_df['reservation_time'] = pd.to_datetime(reservations_df['reservation_time'], errors='coerce')

    # Standardizing column names
    orders_df.columns = [col.lower().replace(" ", "_") for col in orders_df.columns]
    reservations_df.columns = [col.lower().replace(" ", "_") for col in reservations_df.columns]
    print("Data preprocessing completed.")

    # Q5: Feature creation
    # For Orders DataFrame: Add features for order duration (difference between order_date and delivery_date)
    if 'order_date' in orders_df.columns and 'delivery_date' in orders_df.columns:
        orders_df['order_duration'] = (orders_df['delivery_date'] - orders_df['order_date']).dt.days

    # For Reservations DataFrame: Add feature for booking status (based on 'is_confirmed' column)
    if 'is_confirmed' in reservations_df.columns:
        reservations_df['is_confirmed'] = reservations_df['is_confirmed'].astype(int)

    # Example synthetic feature: Create a high_price flag for orders
    if 'total_price' in orders_df.columns:
        orders_df['high_price'] = orders_df['total_price'].apply(lambda x: 1 if x > 500 else 0)

    print("Feature creation completed for both datasets.")

    # Sample of the augmented data with new features
    print("\nOrders DataFrame Sample with Features:")
    print(orders_df.head())

    print("\nReservations DataFrame Sample with Features:")
    print(reservations_df.head())

except requests.exceptions.RequestException as e:
    print(f"Error: fetching data {e}")
except Exception as e:
    print(f"An error occurred: {e}")
