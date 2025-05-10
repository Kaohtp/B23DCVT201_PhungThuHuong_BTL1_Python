import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# Đảm bảo thư mục tồn tại
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

class Paths:
    PART1_RESULTS_PATH = os.path.join(BASE_DIR, 'results.csv')  # Đường dẫn đến file results.csv (ở thư mục chung)
    RAW_TRANSFER_DATA_FILENAME = os.path.join(DATA_DIR, 'raw_transfer_data.csv')
    PROCESSED_TRANSFER_DATA_FILENAME = os.path.join(DATA_DIR, 'processed_transfer_data.csv')
    ESTIMATED_VALUE_OUTPUT_FILENAME = os.path.join(OUTPUT_DIR, 'estimated_player_values.csv')

class Scraping:
    TRANSFER_URL = "https://www.footballtransfers.com/us/players/uk-premier-league"
    WAIT_TIME_SECONDS = 10
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

class Selectors:
    PLAYER_TABLE = "tbody#player-table-body"
    PLAYER_ROW = "tr"
    PLAYER_NAME = "td.td-player div.text > a"
    TEAM_NAME = "td.td-team span.td-team__teamname"
    ETV = "td.text-center > span.player-tag"
    AGE = "td.m-hide.age"
    POSITION = "td.td-player span.sub-text.d-none.d-md-block"
    SKILL = "div.table-skill__skill"
    POTENTIAL = "div.table-skill__pot"
    NEXT_BUTTON_BASE = "button.pagination_next_button"
    NEXT_PAGE_ENABLED = "button.pagination_next_button:not([disabled])"

class Processing:
    MIN_MINUTES_THRESHOLD = 900
    PART1_PLAYER_COLUMN = "Name"  # Tên cột chứa tên cầu thủ trong results.csv
    PART1_MINUTES_COLUMN = "Playing Time: minutes" # Tên cột chứa phút thi đấu trong results.csv
    TARGET_VARIABLE_NAME = "TransferValueEURMillions"