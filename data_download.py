import yfinance as yf
import os
import pandas as pd

df = yf.download("BTC-USD", start="2020-01-01", end="2026-03-20")
df.to_csv("btc_data.csv")
print("Downloaded data.")


# Define the input and output file names
input_csv = "./btc_data.csv"
output_csv = "./btc_data_reordered.csv"

# Define the desired column order
# Note: yfinance typically provides 'Adj Close' as well, so we include it in the new order.
# If 'Adj Close' is not in your original file, you can remove it from the list.


# data = pd.read_csv(input_csv)
# df.columns = df.columns.get_level_values(0)

# # 3. Move 'Date' from the index into a regular column
# df = df.reset_index()

# actual_date_col = "Date" if "Date" in df.columns else "Datetime"

# desired_order = [actual_date_col, "Open", "High", "Low", "Close", "Volume"]
# # Reorder the columns by selecting them in the new sequence
# # This creates a new DataFrame with the specified column order
# df_reordered = df[desired_order]

# # Save the reordered DataFrame to a new CSV file without the pandas index
# df_reordered.to_csv(output_csv, index=False)

# print(df_reordered.head())

# print(f"Columns successfully reordered and saved to {output_csv}")


if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# 3. Move the index (Date/Datetime) into a regular column
df = df.reset_index()

# 4. Identify the date column (it varies by interval)
date_col = "Datetime" if "Datetime" in df.columns else "Date"

# 5. Now reorder will work
desired_order = [date_col, "Open", "High", "Low", "Close", "Volume"]
df_reordered = df[desired_order]

print(df_reordered.head())

df_reordered.to_csv(output_csv, index=False)
