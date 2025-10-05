import pandas as pd

def show_date_range(df, date_column):
    start_date = df[date_column].min().date()
    end_date = df[date_column].max().date()
    days_in_range = (end_date - start_date).days
    print("- Time Period Summary -")
    print(f"Start Date: {start_date}")
    print(f"End Date:   {end_date}")
    print(f"Date Range: {days_in_range} days")
    print("-----------------------")

def calculate_iqr_outliers(df, column_name, k=1.5):
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - k * IQR
    upper_bound = Q3 + k * IQR
    outliers_mask = (df[column_name] < lower_bound) | (df[column_name] > upper_bound)
    outliers_count = int(outliers_mask.sum())
    outliers_rows = df[outliers_mask]
    return outliers_rows, outliers_count