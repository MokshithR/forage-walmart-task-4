import pandas as pd

for i in range(3):
    print(f"\n========== shipping_data_{i}.csv ==========")
    df = pd.read_csv(f"data/shipping_data_{i}.csv")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 10 rows:")
    print(df.head(10))

    print("\n")