import requests
import pandas as pd

def fetch_orders():
    try:
        orders_request = requests.get("http://127.0.0.1:8000/orders") 
        orders_request.raise_for_status()
        orders = orders_request.json()
        
        # If the response is a list, we can directly use it to create a DataFrame
        if isinstance(orders, list):
            return pd.DataFrame(orders)  
        elif isinstance(orders, dict) and 'orders' in orders:
            return pd.DataFrame(orders['orders'])  # Create DataFrame from dictionary if 'orders' key exists
        else:
            print("Unexpected response format")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching orders data: {e}")
        return None

def fetch_reservations():
    try:
        reservations_request = requests.get("http://127.0.0.1:8000/reservations")  # Your endpoint for reservations
        reservations_request.raise_for_status()
        reservations = reservations_request.json()
        
        if isinstance(reservations, list):
            return pd.DataFrame(reservations)  # Create DataFrame from list of reservations
        elif isinstance(reservations, dict) and 'reservations' in reservations:
            return pd.DataFrame(reservations['reservations']) 
        else:
            print("Unexpected response format")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching reservations data: {e}")
        return None

# Fetch the data
orders_df = fetch_orders()
reservations_df = fetch_reservations()

# Check if data is fetched and print the number of rows and columns (shape)
if orders_df is not None:
    print(f"Orders DataFrame fetched: {orders_df.shape[0]} rows, {orders_df.shape[1]} columns")

if reservations_df is not None:
    print(f"Reservations DataFrame fetched: {reservations_df.shape[0]} rows, {reservations_df.shape[1]} columns")


# Check the fetched data
if orders_df is not None:
    print("Orders Dataframe:")
    print(orders_df.head())
    print("Info:")
    print(orders_df.info())

if reservations_df is not None:
    print("Reservations Dataframe:")
    print(reservations_df.head())
    print("Info:")
    print(reservations_df.info())

# Describing the Datasets
if orders_df is not None:
    print("Orders Dataset Description:")
    print(orders_df.describe(include='all'))

if reservations_df is not None:
    print("Reservations Dataset Description:")
    print(reservations_df.describe(include='all'))

# Check missing values after cleaning
print("Missing Values After Cleaning in Orders DataFrame:")
print(orders_df.isnull().sum())

print("Missing Values After Cleaning in Reservations DataFrame:")
print(reservations_df.isnull().sum())

# Replace missing values in orders dataset
orders_df.fillna({"total_amount": orders_df["total_amount"].mean(),
                  "status": "Unknown",
                  "created_at": pd.to_datetime("today"),
                  "updated_at": pd.to_datetime("today")}, inplace=True)

# For reservations dataset
reservations_df.fillna({"party_size": reservations_df["party_size"].mean(),
                         "reservation_time": pd.to_datetime("today"),
                         "contact_number": "Unknown",
                         "is_confirmed": False}, inplace=True)

# Check missing values after cleaning
print("Missing Values After Cleaning in Orders DataFrame:")
print(orders_df.isnull().sum())

print("Missing Values After Cleaning in Reservations DataFrame:")
print(reservations_df.isnull().sum())

# Remove duplicates
orders_df.drop_duplicates(inplace=True)
reservations_df.drop_duplicates(inplace=True)

# Convert datetime columns
orders_df["created_at"] = pd.to_datetime(orders_df["created_at"])
orders_df["updated_at"] = pd.to_datetime(orders_df["updated_at"])

reservations_df["reservation_time"] = pd.to_datetime(reservations_df["reservation_time"])
reservations_df["created_at"] = pd.to_datetime(reservations_df["created_at"])

# Ensure that 'total_amount' is numeric
orders_df["total_amount"] = pd.to_numeric(orders_df["total_amount"], errors="coerce")

# Create new features for orders
orders_df['order_day'] = orders_df['created_at'].dt.day_name()
orders_df['order_hour'] = orders_df['created_at'].dt.hour
orders_df['is_weekend'] = orders_df['order_day'].isin(['Saturday', 'Sunday'])

# Create new features for reservations
reservations_df['reservation_day'] = reservations_df['reservation_time'].dt.day_name()
reservations_df['reservation_hour'] = reservations_df['reservation_time'].dt.hour
reservations_df['is_peak_time'] = reservations_df['reservation_hour'].between(18, 21)

# Display the first few rows to check the new features
print("Orders Dataset with New Features:")
print(orders_df.head())

print("Reservations Dataset with New Features:")
print(reservations_df.head())

# Final Data Shapes and Info
print("Cleaned Orders Dataset Shape:")
print(orders_df.shape)

print("Cleaned Orders Dataset Info:")
print(orders_df.info())

print("Cleaned Reservations Dataset Shape:")
print(reservations_df.shape)

print("Cleaned Reservations Dataset Info:")
print(reservations_df.info())
