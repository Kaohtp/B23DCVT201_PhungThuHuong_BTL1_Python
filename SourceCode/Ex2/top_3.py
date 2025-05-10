import pandas as pd
import numpy as np
import os

# Đọc dữ liệu, tự động xử lý dấu phẩy hàng nghìn
file = "Report/OUTPUT_BAI1/results.csv"
df = pd.read_csv(file, na_values=['N/a'], thousands=',')

# Nếu có cột Age, tách số tuổi ra thành số nguyên
if 'Age' in df.columns:
    df['Age'] = df['Age'].astype(str).str.extract(r'(\d+)').astype(float)

# Các cột thông tin không phải chỉ số
exclude_cols = ['Name', 'Nation', 'Team', 'Position']

# Tự động lấy tất cả các cột còn lại
stats_columns = [col for col in df.columns if col not in exclude_cols]

# Ép kiểu về số cho các cột thống kê, loại bỏ dấu phẩy nếu còn sót
for col in stats_columns:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')

output_filename = "Report/OUTPUT_BAI2/top_3.txt"
with open(output_filename, 'w', encoding='utf-8') as f:
    for col in stats_columns:
        # Bỏ qua cột nếu toàn bộ giá trị là NaN hoặc không phải số
        if df[col].dropna().empty:
            continue
        f.write(f"--- {col} ---\n")
        f.write("-" * (len(col) + 6) + "\n\n")
        top_3 = df.dropna(subset=[col]).sort_values(col, ascending=False)[['Name', 'Team', col]].head(3)
        f.write("Top 3 Player:\n")
        f.write(top_3.to_string(index=False, header=True))
        f.write("\n\n")
        bottom_3 = df.dropna(subset=[col]).sort_values(col, ascending=True)[['Name', 'Team', col]].head(3)
        f.write("Bottom 3 Player:\n")
        f.write(bottom_3.to_string(index=False, header=True))
        f.write("\n\n" + "=" * 50 + "\n\n")
print('Saved results to Report/OUTPUT_BAI2/top_3.txt') 