import pandas as pd
from config import Paths, Processing

def load_and_filter_data(transfer_file, stats_file, min_minutes, player_col_stats, minutes_col_stats, player_col_transfer):
    try:
        df_transfer = pd.read_csv(transfer_file)
        df_stats = pd.read_csv(stats_file)
    except FileNotFoundError as e:
        print(f"Lỗi: Không tìm thấy file: {e}")
        return None

    # Chuẩn hóa tên cột để merge
    df_stats.rename(columns={player_col_stats: player_col_transfer, minutes_col_stats: 'MinutesPlayed'}, inplace=True)

    # Lọc cầu thủ theo số phút thi đấu
    df_filtered_stats = df_stats[df_stats['MinutesPlayed'] > min_minutes][[player_col_transfer]].drop_duplicates()
    print(f"Số lượng cầu thủ có số phút thi đấu > {min_minutes}: {len(df_filtered_stats)}")

    # Merge dữ liệu chuyển nhượng với cầu thủ đã lọc
    df_merged = pd.merge(df_transfer, df_filtered_stats, on=player_col_transfer, how='inner')
    print(f"Kích thước dữ liệu sau khi lọc: {df_merged.shape}")

    return df_merged

if __name__ == "__main__":
    processed_df = load_and_filter_data(
        Paths.RAW_TRANSFER_DATA_FILENAME,
        Paths.PART1_RESULTS_PATH,
        Processing.MIN_MINUTES_THRESHOLD,
        Processing.PART1_PLAYER_COLUMN,
        Processing.PART1_MINUTES_COLUMN,
        "Player"  # Tên cột chung để merge
    )

    if processed_df is not None and not processed_df.empty:
        processed_df.to_csv(Paths.PROCESSED_TRANSFER_DATA_FILENAME, index=False, encoding='utf-8-sig')
        print(f"\nĐã lưu dữ liệu đã xử lý vào: {Paths.PROCESSED_TRANSFER_DATA_FILENAME}")
    elif processed_df is None:
        print("\nKhông thể tiến hành xử lý do lỗi tải file.")
    else:
        print("\nKhông có dữ liệu nào sau khi lọc.")