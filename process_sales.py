import pandas as pd
from pathlib import Path

data_folder = Path("data")
files = [
    data_folder / "daily_sales_data_0.csv",
    data_folder / "daily_sales_data_1.csv",
    data_folder / "daily_sales_data_2.csv",
]

all_data = []

for file in files:
    df = pd.read_csv(file)

    # 统一列名小写
    df.columns = [col.strip().lower() for col in df.columns]

    # 只保留 Pink Morsels
    df = df[df["product"].str.lower() == "pink morsels"]

    # 计算 Sales
    df["sales"] = df["quantity"] * df["price"]

    # 只保留需要的列
    df = df[["sales", "date", "region"]]

    # 重命名列
    df.columns = ["Sales", "Date", "Region"]

    all_data.append(df)

# 合并三个文件
final_df = pd.concat(all_data)

# 输出文件
final_df.to_csv("data/pink_morsels_sales.csv", index=False)

print("Done! File created: data/pink_morsels_sales.csv")
