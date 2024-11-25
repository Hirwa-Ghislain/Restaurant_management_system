# restaurant_analysis.py
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

class SmallRestaurantAnalyzer:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.orders_df = None
        self.reservations_df = None
        self.feedback_df = None

    def fetch_data(self):
        """Fetch and prepare data from all endpoints"""
        try:
            # Fetch orders
            orders_response = requests.get(f"{self.base_url}/orders/")
            self.orders_df = pd.DataFrame(orders_response.json())
            if not self.orders_df.empty:
                self.orders_df['created_at'] = pd.to_datetime(self.orders_df['created_at'])
                self.orders_df['total_amount'] = pd.to_numeric(self.orders_df['total_amount'])

            # Fetch reservations
            reservations_response = requests.get(f"{self.base_url}/reservations/")
            self.reservations_df = pd.DataFrame(reservations_response.json())
            if not self.reservations_df.empty:
                self.reservations_df['reservation_time'] = pd.to_datetime(self.reservations_df['reservation_time'])

            # Fetch feedback
            feedback_response = requests.get(f"{self.base_url}/feedback/")
            self.feedback_df = pd.DataFrame(feedback_response.json())
            if not self.feedback_df.empty:
                self.feedback_df['created_at'] = pd.to_datetime(self.feedback_df['created_at'])

        except Exception as e:
            print(f"Error fetching data: {str(e)}")

    def analyze_orders(self):
        """Analyze order patterns"""
        if self.orders_df is None or self.orders_df.empty:
            print("No orders data available")
            return

        print("\n=== Detailed Order Analysis ===")
        
        # Order Overview
        print("\nOrder Overview:")
        print(f"Total Orders: {len(self.orders_df)}")
        print(f"Total Revenue: ${self.orders_df['total_amount'].sum():.2f}")
        print(f"Average Order Value: ${self.orders_df['total_amount'].mean():.2f}")
        
        # Order Status
        print("\nOrder Status Breakdown:")
        status_counts = self.orders_df['status'].value_counts()
        for status, count in status_counts.items():
            print(f"{status}: {count} orders ({count/len(self.orders_df)*100:.1f}%)")

        # Items Analysis
        print("\nMost Ordered Items:")
        all_items = []
        for items_str in self.orders_df['items']:
            items_list = [item.strip() for item in items_str.split(',')]
            all_items.extend(items_list)
        
        item_counts = pd.Series(all_items).value_counts()
        for item, count in list(item_counts.items())[:5]:  # Convert to list before slicing
            print(f"{item}: {count} times")

        # Time Analysis
        self.orders_df['hour'] = self.orders_df['created_at'].dt.hour
        self.orders_df['day_name'] = self.orders_df['created_at'].dt.day_name()
        
        print("\nOrders by Day:")
        day_counts = self.orders_df['day_name'].value_counts()
        for day, count in day_counts.items():
            print(f"{day}: {count} orders")

        # Revenue Analysis
        print("\nRevenue Analysis:")
        max_order = self.orders_df.loc[self.orders_df['total_amount'].idxmax()]
        print(f"Highest Order Amount: ${max_order['total_amount']:.2f} ({max_order['customer_name']})")
        print(f"Average Order Value: ${self.orders_df['total_amount'].mean():.2f}")
        print(f"Median Order Value: ${self.orders_df['total_amount'].median():.2f}")

    def analyze_reservations(self):
        """Analyze reservation patterns"""
        if self.reservations_df is None or self.reservations_df.empty:
            print("No reservations data available")
            return

        print("\n=== Detailed Reservation Analysis ===")
        
        # Basic Stats
        print("\nReservation Overview:")
        print(f"Total Reservations: {len(self.reservations_df)}")
        print(f"Average Party Size: {self.reservations_df['party_size'].mean():.1f}")
        print(f"Total Expected Guests: {self.reservations_df['party_size'].sum()}")
        
        # Time Analysis
        self.reservations_df['day_name'] = self.reservations_df['reservation_time'].dt.day_name()
        self.reservations_df['hour'] = self.reservations_df['reservation_time'].dt.hour
        
        print("\nReservations by Day:")
        day_counts = self.reservations_df['day_name'].value_counts()
        for day, count in day_counts.items():
            print(f"{day}: {count} reservations")
        
        print("\nPopular Hours:")
        hour_counts = self.reservations_df['hour'].value_counts().sort_index()
        for hour, count in hour_counts.items():
            print(f"{hour:02d}:00: {count} reservations")

        # Party Size Analysis
        print("\nParty Size Analysis:")
        print(f"Largest Party: {self.reservations_df['party_size'].max()} people")
        print(f"Most Common Party Size: {self.reservations_df['party_size'].mode().iloc[0]} people")

    def analyze_feedback(self):
        """Analyze customer feedback"""
        if self.feedback_df is None or self.feedback_df.empty:
            print("No feedback data available")
            return

        print("\n=== Detailed Feedback Analysis ===")
        
        # Basic Stats
        print("\nFeedback Overview:")
        print(f"Total Reviews: {len(self.feedback_df)}")
        print(f"Average Rating: {self.feedback_df['rating'].mean():.2f}/5.0")
        
        # Rating Distribution
        print("\nRating Distribution:")
        rating_counts = self.feedback_df['rating'].value_counts().sort_index()
        for rating, count in rating_counts.items():
            print(f"{rating} stars: {count} reviews ({count/len(self.feedback_df)*100:.1f}%)")

        # Comment Analysis
        if 'comment' in self.feedback_df.columns:
            comment_lengths = self.feedback_df['comment'].str.len()
            print(f"\nComment Analysis:")
            print(f"Average Comment Length: {comment_lengths.mean():.0f} characters")
            print(f"Longest Comment: {comment_lengths.max()} characters")
            print(f"Shortest Comment: {comment_lengths.min()} characters")

    def make_insights(self):
        """Generate business insights from the data"""
        print("\n=== Business Insights ===")
        
        if not self.orders_df.empty:
            # Popular times
            busy_hours = self.orders_df['created_at'].dt.hour.value_counts().sort_index()
            peak_hour = busy_hours.index[busy_hours.argmax()]
            print(f"\nPeak Order Hour: {peak_hour:02d}:00")
            
            # Revenue patterns
            avg_revenue = self.orders_df['total_amount'].mean()
            print(f"Average Revenue per Order: ${avg_revenue:.2f}")
            
            # Status patterns
            completion_rate = (self.orders_df['status'] == 'completed').mean() * 100
            print(f"Order Completion Rate: {completion_rate:.1f}%")

        if not self.reservations_df.empty:
            # Reservation patterns
            avg_party = self.reservations_df['party_size'].mean()
            total_guests = self.reservations_df['party_size'].sum()
            print(f"\nAverage Party Size: {avg_party:.1f} people")
            print(f"Total Expected Guests: {total_guests}")

        if not self.feedback_df.empty:
            # Customer satisfaction
            avg_rating = self.feedback_df['rating'].mean()
            satisfaction_rate = (self.feedback_df['rating'] >= 4).mean() * 100
            print(f"\nCustomer Satisfaction:")
            print(f"Average Rating: {avg_rating:.1f}/5.0")
            print(f"Satisfaction Rate (≥4 stars): {satisfaction_rate:.1f}%")

def main():
    analyzer = SmallRestaurantAnalyzer()
    
    print("Fetching and analyzing data...")
    analyzer.fetch_data()
    
    # Run analyses
    analyzer.analyze_orders()
    analyzer.analyze_reservations()
    analyzer.analyze_feedback()
    analyzer.make_insights()

if __name__ == "__main__":
    main()