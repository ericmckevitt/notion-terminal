from notion_football import fetch_upcoming_matches
from datetime import datetime

def main():
    today = datetime.today().strftime("%Y-%m-%d")
    print(f"\n📅 Upcoming Matches (from {today}):\n")
    matches = fetch_upcoming_matches()
    for match in matches:
        print(f"⚽ {match['name']}")
        print(f"   🏆 {match['league']}")
        print(f"   🕒 {match['date']}\n")

if __name__ == "__main__":
    main()
