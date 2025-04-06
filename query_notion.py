import argparse
from notion_football import fetch_upcoming_matches
from datetime import datetime
from tabulate import tabulate

TEAM_FILTERS = {
    "mc": "Man City",
    "rm": "Real Madrid"
}

def main():
    parser = argparse.ArgumentParser(description="Query Notion football database.")
    parser.add_argument("--team", help="Filter by team abbreviation (e.g., mc, rm)")
    args = parser.parse_args()

    team_name = TEAM_FILTERS.get(args.team.lower()) if args.team else None
    today = datetime.today().strftime("%Y-%m-%d")

    print(f"\n📅 Upcoming Matches (from {today}):\n")

    matches = fetch_upcoming_matches(team_name=team_name)
    # for match in matches:
    #     print(f"⚽ {match['name']}")
    #     print(f"   🏆 {match['league']}")
    #     print(f"   🕒 {match['date']}\n")
    table_data = [(m['name'], m['league'], m['date']) for m in matches]
    headers = ["Match", "League", "Date"]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

if __name__ == "__main__":
    main()
