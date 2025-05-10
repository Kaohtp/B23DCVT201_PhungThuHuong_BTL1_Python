#''Tính median, mean, std cho từng chỉ số (toàn giải và từng đội), lưu vào results2.csv đúng format.
import pandas as pd
import numpy as np
import csv

# Đọc dữ liệu
file = 'Report/OUTPUT_BAI1/results.csv'
df = pd.read_csv(file, na_values=['N/a'])

# Các cột thông tin không phải chỉ số
exclude_cols = ['Name', 'Nation', 'Team', 'Position', 'Age']

# Tự động lấy tất cả các cột còn lại
stats_columns = [col for col in df.columns if col not in exclude_cols]

# Ép kiểu về số cho các cột thống kê
for col in stats_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Tính toán cho toàn bộ giải
all_row = ['all']
for col in stats_columns:
    all_row.extend([
        df[col].median(),
        df[col].mean(),
        df[col].std()
    ])

# Tính toán cho từng đội
team_rows = []
for team in sorted(df['Team'].dropna().unique()):
    team_data = df[df['Team'] == team]
    row = [team]
    for col in stats_columns:
        row.extend([
            team_data[col].median(),
            team_data[col].mean(),
            team_data[col].std()
        ])
    team_rows.append(row)

# Header
header = ['Team']
for col in stats_columns:
    header.extend([
        f'Median of {col}',
        f'Mean of {col}',
        f'Std of {col}'
    ])

# Ghi ra file CSV
with open('Report/OUTPUT_BAI2/results2.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(all_row)
    writer.writerows(team_rows)
print('Saved results to Report/OUTPUT_BAI2/results2.csv')