# scrape_player_data.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, csv, re, pandas as pd
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
import traceback
import os
import unicodedata
import random
import sys
sys.stdout.reconfigure(encoding='utf-8')


MAIN_URL = "https://www.footballtransfers.com/us/players/uk-premier-league"
OUTPUT_CSV_PATH = "Report/OUTPUT_BAI4/player_transfer_data.csv"
MIN_PLAYING_TIME = 900
WAIT_TIMEOUT = 15
SHORT_WAIT_TIMEOUT = 7
TIME_SLEEP_AFTER_PAGE_LOAD = 3
TIME_SLEEP_DETAIL_PAGE = 3
NEXT_BUTTON_SELECTOR = "button.pagination_next_button:not([disabled])"

def normalize_name(name: str) -> str:
    if not isinstance(name, str):
        return ""
    nfkd_form = unicodedata.normalize('NFKD', name)
    normalized = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    return normalized.lower().strip()

def parse_etv(value_str):
    if not value_str or value_str.lower() in ['n/a', 'na', '']:
        return None
    text = re.sub(r'[€£$ ,]', '', value_str.lower())
    multiplier = 1e6 if 'm' in text else (1e3 if 'k' in text else 1.0)
    numeric_part = text.replace('m', '').replace('k', '')
    try:
        return round(float(numeric_part) * multiplier / 1e6, 2)
    except ValueError:
        return None

def has_played_enough(results_csv_path, player_name, min_minutes):
    try:
        df = pd.read_csv(results_csv_path)
        if 'Name' not in df.columns or 'Playing Time: minutes' not in df.columns:
            print(f"Warning: Missing 'Name' or 'Playing Time: minutes' column in '{results_csv_path}'.")
            return False
        player_row = df[df['Name'].apply(normalize_name) == normalize_name(player_name)]
        if not player_row.empty:
            minutes_str = str(player_row['Playing Time: minutes'].iloc[0]).replace(',', '')
            try:
                minutes = int(float(minutes_str))
                return minutes > min_minutes
            except ValueError:
                return False
        return False
    except FileNotFoundError:
        print(f"Warning: File not found: '{results_csv_path}'. Cannot verify playing time.")
        return False
    except Exception as e:
        print(f"Error checking playing time: {e}")
        return False

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument("--headless") # Uncomment for headless browsing
driver = webdriver.Chrome(options=options)

all_results = []
results_csv_path = "Report/OUTPUT_BAI1/results.csv" # Assuming this file exists

try:
    print(f"Loading the main page: {MAIN_URL}")
    driver.get(MAIN_URL)
    WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "tbody#player-table-body"))
    )
    print("Player table loaded successfully.")
    time.sleep(TIME_SLEEP_AFTER_PAGE_LOAD)

    page_num = 1
    total_players_scraped = 0

    while True:
        print(f"\nProcessing page {page_num}...")
        try:
            WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tbody#player-table-body"))
            )
        except TimeoutException:
            print(f"Timeout waiting for player table on page {page_num}. Moving to the next step.")
            break

        rows_on_current_page = driver.find_elements(By.CSS_SELECTOR, "tbody#player-table-body tr")
        print(f"Found {len(rows_on_current_page)} players on page {page_num}.")
        if not rows_on_current_page and page_num > 1:
            print("No players found on this page, assuming end of data.")
            break

        for i, row in enumerate(rows_on_current_page):
            name, detail_url, team, age, pos = "N/A", None, "N/A", "N/A", "N/A"
            current_etv_text, highest_etv_text = "N/A", "N/A"
            current_etv_parsed, highest_etv_parsed = None, None

            try:
                try:
                    link_elem = row.find_element(By.CSS_SELECTOR, "td.td-player div.text > a")
                    name = link_elem.text.strip()
                    detail_url = link_elem.get_attribute("href")
                except NoSuchElementException:
                    continue

                if not name or not detail_url:
                    continue

                if not has_played_enough(results_csv_path, name, MIN_PLAYING_TIME):
                    print(f"Skipping {name} - less than {MIN_PLAYING_TIME} minutes played.")
                    continue

                try:
                    print(f"Processing: {name} (Row {i+1} - Page {page_num})")
                except UnicodeEncodeError:
                    print(f"Processing: (Lỗi tên) (Hàng {i+1} - Trang {page_num})")

                try:
                    team = row.find_element(By.CSS_SELECTOR, "td.td-team span.td-team__teamname").text.strip()
                except NoSuchElementException:
                    team = "N/A"

                try:
                    age_raw_text = row.find_element(By.CSS_SELECTOR, "td.m-hide.age").text.strip()
                    age = age_raw_text.split("-")[0].strip()
                except NoSuchElementException:
                    age = "N/A"

                try:
                    pos = row.find_element(By.CSS_SELECTOR, "td.td-player span.sub-text").text.strip()
                except NoSuchElementException:
                    pos = "N/A"

                try:
                    etv_elem = row.find_element(By.CSS_SELECTOR, "span.player-tag")
                    current_etv_text = etv_elem.text.strip()
                except NoSuchElementException:
                    current_etv_text = "N/A"

                current_etv_parsed = parse_etv(current_etv_text)

                # Highest ETV from detail page
                main_window_handle = driver.current_window_handle
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(detail_url)
                time.sleep(TIME_SLEEP_DETAIL_PAGE)

                highest_etv_text = "N/A"
                divs = driver.find_elements(By.CSS_SELECTOR, "div.d-col")
                for div_element in divs:
                    try:
                        label = div_element.find_element(By.CSS_SELECTOR, "span.txt")
                        if "Highest ETV" in label.text:
                            value = div_element.find_element(By.CSS_SELECTOR, "span.player-tag")
                            highest_etv_text = value.text.strip()
                            break
                    except NoSuchElementException:
                        continue

                driver.close()
                driver.switch_to.window(main_window_handle)

                highest_etv_parsed = parse_etv(highest_etv_text)
                if highest_etv_parsed is None:
                    highest_etv_parsed = current_etv_parsed

                all_results.append({
                    "Player": name,
                    "Team": team,
                    "Age": age,
                    "Position": pos,
                    "TransferValue_EUR_Millions": current_etv_parsed,
                    "Highest_ETV_EUR_Millions": highest_etv_parsed
                })
                total_players_scraped += 1
                try:
                    print(f"Collected data for {name}: Current ETV = {current_etv_parsed}MEUR, Highest = {highest_etv_parsed}MEUR")
                except UnicodeEncodeError:
                    print(f"Collected data for (Lỗi tên): Current ETV = {current_etv_parsed}MEUR, Highest = {highest_etv_parsed}MEUR")
                time.sleep(random.uniform(0.5, 1.2))

            except TimeoutException as e_timeout_row:
                try:
                    print(f"Timeout processing details for {name if name != 'N/A' else f'row {i+1}'}: {e_timeout_row}. Skipping.")
                except UnicodeEncodeError:
                    print(f"Timeout processing details for (Lỗi tên): {e_timeout_row}. Skipping.")
                if driver.current_window_handle != main_window_handle and len(driver.window_handles) > 1:
                    driver.close()
                    driver.switch_to.window(main_window_handle)
                continue
            except Exception as e_row:
                try:
                    print(f"Error processing details for {name if name != 'N/A' else f'row {i+1}'}: {type(e_row).__name__} - {e_row}. Skipping.")
                except UnicodeEncodeError:
                    print(f"Error processing details for (Lỗi tên): {type(e_row).__name__} - {e_row}. Skipping.")
                if driver.current_window_handle != main_window_handle and len(driver.window_handles) > 1:
                    driver.close()
                    driver.switch_to.window(main_window_handle)
                continue

        try:
            next_button = WebDriverWait(driver, SHORT_WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, NEXT_BUTTON_SELECTOR))
            )
            print(f"Found 'Next page' button. Navigating to page {page_num + 1}...")
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(0.5)
            try:
                next_button.click()
            except ElementClickInterceptedException:
                print("Click intercepted, trying JavaScript click...")
                driver.execute_script("arguments[0].click();", next_button)

            page_num += 1
            time.sleep(TIME_SLEEP_AFTER_PAGE_LOAD)

        except TimeoutException:
            print("Could not find 'Next page' button or reached the end. Finishing data collection.")
            break
        except Exception as e_pagination:
            print(f"Error during pagination: {type(e_pagination).__name__} - {e_pagination}")
            traceback.print_exc()
            break

    print("\nData collection complete.")
    print(f"Total players scraped (with > {MIN_PLAYING_TIME} mins): {total_players_scraped}")

except Exception as e_global:
    print(f"A critical error occurred during scraping: {e_global}")
    traceback.print_exc()
finally:
    if 'driver' in locals() and driver:
        driver.quit()
        print("\nBrowser closed.")

if all_results:
    df_output = pd.DataFrame(all_results)
    output_dir = os.path.dirname(OUTPUT_CSV_PATH)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    df_output.to_csv(OUTPUT_CSV_PATH, index=False, encoding="utf-8-sig")
    print(f"Scraped data saved to: {OUTPUT_CSV_PATH}")
else:
    print("No data was scraped to save.")

print("\nScript finished.")