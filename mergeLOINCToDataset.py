import csv

import pandas as pd

# 读取第一个CSV文件
df1 = pd.read_csv(r'labeled_result.csv')

# 读取第二个CSV文件(英文/中文Loinc标准词汇表)，设置 low_memory=False 来处理 DtypeWarning
df2 = pd.read_csv(r'Loinc_2.80/LoincTable/Loinc.csv', low_memory=False)
# df2 = pd.read_csv(r'Loinc_2.80/AccessoryFiles/LinguisticVariants/zhCN5LinguisticVariant.csv', low_memory=False)

# 清理列名中的双引号
df2.columns = df2.columns.str.replace('"', '')

# 选择需要的列
df2_selected = df2[['LOINC_NUM','COMPONENT','PROPERTY','SYSTEM','SCALE_TYP','TIME_ASPCT','METHOD_TYP','CLASS','RELATEDNAMES2']]
df1.rename(columns={'LOINC': 'LOINC_NUM'}, inplace=True)
df_merged = pd.merge(df1, df2_selected, on='LOINC_NUM', how='inner')

# 修复第二列的数据格式为字符串（防止1 -> 1.0）
# 你可以按列名定位（更安全），假设第二列为 'XXX'，否则用iloc
second_col = df_merged.columns[1]
df_merged[second_col] = df_merged[second_col].apply(lambda x: str(int(x)) if isinstance(x, float) and x.is_integer() else x)

# 写入文件
df_merged.to_csv(r'golden.csv', index=False, quoting=csv.QUOTE_ALL)

print("CSV文件合并完成！")
