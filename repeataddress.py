import pandas as pd

def main():
    # === 可修改参数 ===
    input_csv_path = "input.csv"             # 输入文件路径
    dedup_columns = ["col1","col2"]       # 用于去重的列，可多列
    output_csv_path = "output.csv"          # 输出文件路径

    # === 读取CSV ===
    df = pd.read_csv(input_csv_path)
    print(f"原始数据行数: {len(df)}")

    # === 去重 ===
    df_dedup = df.drop_duplicates(subset=dedup_columns)
    print(f"去重后数据行数: {len(df_dedup)}")

    # === 写入CSV ===
    df_dedup.to_csv(output_csv_path, index=False)
    print(f"去重结果已保存至: {output_csv_path}")

if __name__ == "__main__":
    main()
