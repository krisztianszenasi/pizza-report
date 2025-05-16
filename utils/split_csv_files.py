import sys
import os
import pandas as pd


def main() -> int:
    # Load data
    orders = pd.read_csv("orders.csv", parse_dates=["date"])
    order_details = pd.read_csv("order_details.csv")

    # Create a 'year_month' column
    orders["year_month"] = orders["date"].dt.to_period("M")

    # Output directory
    os.makedirs("monthly_chunks", exist_ok=True)

    # Process all months
    for year_month, orders_month in orders.groupby("year_month"):
        ym_str = str(year_month).replace("-", "_")  # e.g. '2015_01'
        
        # Get relevant order_ids
        month_order_ids = orders_month["order_id"].unique()
        
        # Filter order_details
        details_month = order_details[order_details["order_id"].isin(month_order_ids)]

        # Drop helper year month
        orders_to_save = orders_month.drop(columns=["year_month"])
        
        # Save files
        orders_to_save.to_csv(f"monthly_chunks/orders_{ym_str}.csv", index=False)
        details_month.to_csv(f"monthly_chunks/order_details_{ym_str}.csv", index=False)
        
        print(f"Saved: orders_{ym_str}.csv and order_details_{ym_str}.csv")
    return 0


if __name__ == '__main__':
    sys.exit(main())