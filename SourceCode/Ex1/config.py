# config.py

BASE_URL = "https://fbref.com/en/comps/9/"
SEASON_SUFFIX = "Premier-League-Stats"
CSV_FILE = "Report/OUTPUT_BAI1/results.csv"
MIN_MINUTES = 90
WAIT_TIMEOUT = 10

# Cấu hình các bảng và trường cần lấy
TABLES = [
    {
        "url": "stats/",
        "table_id": "stats_standard",
        "fields": [
            ("Name", "player"),
            ("Nation", "nationality"),
            ("Team", "team"),
            ("Position", "position"),
            ("Age", "age"),
            ("Playing Time: matches played", "games"),
            ("Playing Time: starts", "games_starts"),
            ("Playing Time: minutes", "minutes"),
            ("Performance: goals", "goals"),
            ("Performance: assists", "assists"),
            ("Performance: yellow cards", "cards_yellow"),
            ("Performance: red cards", "cards_red"),
            ("Expected: expected goals (xG)", "xg"),
            ("Expected: expedted Assist Goals (xAG)", "xg_assist"),
            ("Progression: PrgC", "progressive_carries"),
            ("Progression: PrgP", "progressive_passes"),
            ("Progression: PrgR", "progressive_passes_received"),
            ("Per 90 minutes: Gls", "goals_per90"),
            ("Per 90 minutes: Ast", "assists_per90"),
            ("Per 90 minutes: xG", "xg_per90"),
            ("Per 90 minutes: xGA", "xg_assist_per90"),
        ]
    },
    {
        "url": "keepers/",
        "table_id": "stats_keeper",
        "fields": [
            ("Performance: goals against per 90mins (GA90)", "gk_goals_against_per90"),
            ("Performance: Save%", "gk_save_pct"),
            ("Performance: CS%", "gk_clean_sheets_pct"),
            ("Penalty Kicks: penalty kicks Save%", "gk_pens_save_pct"),
        ]
    },
    {
        "url": "shooting/",
        "table_id": "stats_shooting",
        "fields": [
            ("Standard: shoots on target percentage (SoT%)", "shots_on_target_pct"),
            ("Standard: Shoot on Target per 90min (SoT/90)", "shots_on_target_per90"),
            ("Standard: goals/shot (G/sh)", "goals_per_shot"),
            ("Standard: average shoot distance (Dist)", "average_shot_distance"),
        ]
    },
    {
        "url": "passing/",
        "table_id": "stats_passing",
        "fields": [
            ("Total: passes completed (Cmp)", "passes_completed"),
            ("Total: Pass completion (Cmp%)", "passes_pct"),
            ("Total: progressive passing distance (TotDist)", "passes_progressive_distance"),
            ("Short: Pass completion (Cmp%)", "passes_pct_short"),
            ("Medium: Pass completion (Cmp%)", "passes_pct_medium"),
            ("Long: Pass completion (Cmp%)", "passes_pct_long"),
            ("Expected: key passes (KP)", "assisted_shots"),
            ("Expected: pass into final third (1/3)", "passes_into_final_third"),
            ("Expected: pass into penalty area (PPA)", "passes_into_penalty_area"),
            ("Expected: CrsPA", "crosses_into_penalty_area"),
            ("Expected: PrgP", "progressive_passes"),
        ]
    },
    {
        "url": "gca/",
        "table_id": "stats_gca",
        "fields": [
            ("SCA: SCA", "sca"),
            ("SCA: SCA90", "sca_per90"),
            ("GCA: GCA", "gca"),
            ("GCA: GCA90", "gca_per90"),
        ]
    },
    {
        "url": "defense/",
        "table_id": "stats_defense",
        "fields": [
            ("Tackles: Tkl", "tackles"),
            ("Tackles: TklW", "tackles_won"),
            ("Challenges: Att", "challenges"),
            ("Challenges: Lost", "challenges_lost"),
            ("Blocks: Blocks", "blocks"),
            ("Blocks: Sh", "blocked_shots"),
            ("Blocks: Pass", "blocked_passes"),
            ("Blocks: Int", "interceptions"),
        ]
    },
    {
        "url": "possession/",
        "table_id": "stats_possession",
        "fields": [
            ("Touches: Touches", "touches"),
            ("Touches: Def Pen", "touches_def_pen_area"),
            ("Touches: Def 3rd", "touches_def_3rd"),
            ("Touches: Mid 3rd", "touches_mid_3rd"),
            ("Touches: Att 3rd", "touches_att_3rd"),
            ("Touches: Att Pen", "touches_att_pen_area"),
            ("Take-Ons: Att", "take_ons"),
            ("Take-Ons: Succ%", "take_ons_won_pct"),
            ("Take-Ons: Tkld%", "take_ons_tackled_pct"),
            ("Carries: Carries", "carries"),
            ("Carries: ProDist", "carries_progressive_distance"),
            ("Carries: ProgC", "progressive_carries"),
            ("Carries: 1/3", "carries_into_final_third"),
            ("Carries: CPA", "carries_into_penalty_area"),
            ("Carries: Mis", "miscontrols"),
            ("Carries: Dis", "dispossessed"),
            ("Receiving: Rec", "passes_received"),
            ("Receiving: PrgR", "progressive_passes_received"),
        ]
    },
    {
        "url": "misc/",
        "table_id": "stats_misc",
        "fields": [
            ("Performance: Fls", "fouls"),
            ("Performance: Fld", "fouled"),
            ("Performance: Off", "offsides"),
            ("Performance: Crs", "crosses"),
            ("Performance: Recov", "ball_recoveries"),
            ("Aerial Duels: Won", "aerials_won"),
            ("Aerial Duels: Lost", "aerials_lost"),
            ("Aerial Duels: Won%", "aerials_won_pct"),
        ]
    }
]

# Thứ tự cột xuất ra file CSV
CSV_COLUMNS = [field[0] for table in TABLES for field in table["fields"]]