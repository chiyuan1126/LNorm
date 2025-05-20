import pandas as pd
import re

def normalize(text):
    """模糊匹配用的标准化函数：去空格、引号、连字符，小写化"""
    if pd.isna(text):
        return ""
    return re.sub(r'[\s"\'\-]', '', str(text)).lower()

def build_match_key(row, columns):
    """对多列合并后做标准化"""
    return ''.join([normalize(row[col]) for col in columns])

def merge_csv_by_fuzzy_columns(file1, file2, on_columns_1, on_columns_2, columns_to_add, output_matched_file, output_unmatched_file):
    # 读取CSV
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # 生成模糊匹配键
    df1['_match_key'] = df1.apply(lambda row: build_match_key(row, on_columns_1), axis=1)
    df2['_match_key'] = df2.apply(lambda row: build_match_key(row, on_columns_2), axis=1)

    # 合并匹配记录
    matched_rows = []
    unmatched_rows = []

    for _, row1 in df1.iterrows():
        key = row1['_match_key']
        matched = df2[df2['_match_key'] == key]

        if not matched.empty:
            for _, row2 in matched.iterrows():
                new_row = row1.drop(labels=['_match_key']).to_dict()
                for col in columns_to_add:
                    new_row[f"{col}_from_2"] = row2[col]
                matched_rows.append(new_row)
        else:
            unmatched_rows.append(row1.drop(labels=['_match_key']).to_dict())

    # 输出匹配成功的
    matched_df = pd.DataFrame(matched_rows)
    matched_df.to_csv(output_matched_file, index=False)

    # 输出未匹配成功的
    unmatched_df = pd.DataFrame(unmatched_rows)
    unmatched_df.to_csv(output_unmatched_file, index=False)

    print(f"✅ 匹配成功的已保存至 {output_matched_file}")
    print(f"✅ 未匹配到的已保存至 {output_unmatched_file}")

# === 示例用法 ===
merge_csv_by_fuzzy_columns(
    file1="data_row_unmerge.csv",
    file2="jsudata.csv",
    on_columns_1=["项目名称","平台名称"],     # 1.csv 中用于匹配的列名（支持多列）
    on_columns_2=["REPORT_ITEM_NAME","ITEM_NAME"],     # 2.csv 中用于匹配的列名（支持多列）
    columns_to_add=["UNITS","PRINT_CONTEXT","SPECIMEN"],  # 从 2.csv 中提取合并的列
    output_matched_file = "data_merge.csv",
    output_unmatched_file = "data_unmerge.csv"
)
