#Xác định đội có chỉ số cao nhất cho từng chỉ số, đánh giá đội mạnh nhất mùa giải.
import pandas as pd
import numpy as np
import config as config

def classify_stat(stat_name):
    if stat_name in config.IGNORE_STATS:
        return 'ignore'
    if stat_name in config.GOOD_STATS:
        return 'good'
    if stat_name in config.BAD_STATS:
        return 'bad'
    return 'uncategorized'

def main():
    df = pd.read_csv(config.CSV_PATH, na_values=config.NA_VALUES)
    stats_columns = [col for col in df.columns if col != config.TEAM_COLUMN and col not in config.IGNORE_STATS]
    results = {}
    lead_counts = {}
    print("\nTeams with the highest (or lowest for bad stats) value for each statistic:")
    for col in stats_columns:
        stat_type = classify_stat(col)
        numeric_col = pd.to_numeric(df[col], errors='coerce')
        if numeric_col.isnull().all():
            continue
        if stat_type == 'good' or stat_type == 'uncategorized':
            idx = numeric_col.idxmax()
            best_value = numeric_col.max()
        elif stat_type == 'bad':
            idx = numeric_col.idxmin()
            best_value = numeric_col.min()
        else:
            continue
        team = df.loc[idx, config.TEAM_COLUMN]
        results[col] = (team, best_value, stat_type)
        lead_counts[team] = lead_counts.get(team, 0) + 1
        print(f"{col} [{stat_type.upper()}]: {team} (value: {best_value})")
    print("\nSummary ranking (number of times leading in statistics):")
    for team, count in sorted(lead_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{team}: {count} top statistics")
    if lead_counts:
        best_team = max(lead_counts.items(), key=lambda x: x[1])[0]
        print(f"\n=> Best performing team of the season (by statistics): {best_team}")

if __name__ == "__main__":
    main() 