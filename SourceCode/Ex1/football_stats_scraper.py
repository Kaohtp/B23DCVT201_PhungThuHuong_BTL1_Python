import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from config import BASE_URL, SEASON_SUFFIX, TABLES, CSV_FILE, MIN_MINUTES, WAIT_TIMEOUT, CSV_COLUMNS

def get_first_name(full_name):
    if not isinstance(full_name, str) or not full_name.strip():
        return ""
    return full_name.split()[0]

def fetch_table(driver, url, table_id, fields):
    driver.get(url)
    WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, table_id)))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table", id=table_id)
    rows = table.find("tbody").find_all("tr")
    data = {}
    for row in rows:
        player_cell = row.find("td", {"data-stat": "player"})
        team_cell = row.find("td", {"data-stat": "team"})
        if not player_cell or not team_cell:
            continue
        player_name = player_cell.text.strip()
        team_name = team_cell.text.strip()
        key = (player_name, team_name)
        if key not in data:
            data[key] = {}
        for col, stat in fields:
            cell = row.find("td", {"data-stat": stat})
            val = cell.text.strip() if cell else "N/a"
            data[key][col] = val if val else "N/a"
    return data

def combine_data(list_of_dicts):
    combined = {}
    for d in list_of_dicts:
        for key, val in d.items():
            if key not in combined:
                combined[key] = val
            else:
                combined[key].update(val)
    return combined

def main():
    driver = webdriver.Chrome()
    all_tables = []
    for table in TABLES:
        url = BASE_URL + table["url"] + SEASON_SUFFIX
        table_data = fetch_table(driver, url, table["table_id"], table["fields"])
        all_tables.append(table_data)
        time.sleep(1)
    driver.quit()

    merged = combine_data(all_tables)
    # Lọc theo số phút
    filtered = []
    for player in merged.values():
        min_str = player.get("Playing Time: minutes", "0").replace(",", "")
        try:
            mins = int(min_str)
        except:
            mins = 0
        if mins > MIN_MINUTES:
            filtered.append(player)
    # Sắp xếp theo tên
    filtered.sort(key=lambda x: get_first_name(x.get("Name", "")))
    # Đảm bảo đủ cột, điền "N/a" nếu thiếu
    for row in filtered:
        for col in CSV_COLUMNS:
            if col not in row:
                row[col] = "N/a"
    df = pd.DataFrame(filtered, columns=CSV_COLUMNS)

    # Loại bỏ dấu phẩy trong tất cả các cột số (trừ các cột thông tin)
    exclude_cols = ['Name', 'Nation', 'Team', 'Position']
    for col in df.columns:
        if col not in exclude_cols:
            df[col] = df[col].astype(str).str.replace(',', '')

    df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
    print(f"Saved {len(df)} players to {CSV_FILE}")

if __name__ == "__main__":
    main()