# import pandas as pd
# from sqlalchemy import create_engine
# import psycopg2
# from sqlalchemy.exc import IntegrityError

# # Database connection
# engine = create_engine('postgresql://postgres:hirwa56@localhost:5432/restaurant_db')

# # Read the CSV file into a DataFrame
# orders_df = pd.read_csv('orders_data.csv')

# # Ensure the 'id' column is excluded so the DB can auto-generate the 'id' value
# orders_df = orders_df.drop(columns=['id'], errors='ignore')

# # Convert datetime columns to the correct format (if needed)
# orders_df['created_at'] = pd.to_datetime(orders_df['created_at'])
# orders_df['updated_at'] = pd.to_datetime(orders_df['updated_at'])

# # Insert data into the 'orders' table
# try:
#     orders_df.to_sql('orders', engine, if_exists='append', index=False)
#     print("Data inserted successfully.")
# except IntegrityError as e:
#     print(f"Error occurred: {e}")


import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

# Database connection
engine = create_engine('postgresql://postgres:hirwa56@localhost:5432/restaurant_db')

# Read the reservations data from the CSV file
reservations_df = pd.read_csv('reservations_data.csv')

# Convert datetime columns to the correct format
reservations_df['reservation_time'] = pd.to_datetime(reservations_df['reservation_time'])
reservations_df['created_at'] = pd.to_datetime(reservations_df['created_at'])

# Ensure the 'id' column is excluded so the DB can auto-generate it
reservations_df = reservations_df.drop(columns=['id'], errors='ignore')

# Insert data into the 'reservations' table
try:
    reservations_df.to_sql('reservations', engine, if_exists='append', index=False)
    print("Reservations inserted successfully.")
except IntegrityError as e:
    print(f"Error occurred while inserting reservations: {e}")
