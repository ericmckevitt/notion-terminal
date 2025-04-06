from notion_client import Client
from datetime import datetime
import os

# notion_football.py

def fetch_upcoming_matches(team_name=None):
    notion = Client(auth=os.environ["NOTION_API_TOKEN"])
    database_id = "d78e531fc51a4f3b870f9773d6b0ee85"
    today = datetime.today().strftime("%Y-%m-%d")

    filters = {
        "property": "Date",
        "date": {"on_or_after": today}
    }

    if team_name:
        filters = {
            "and": [
                filters,
                {
                    "property": "Name",
                    "rich_text": {"contains": team_name}
                }
            ]
        }

    response = notion.databases.query(
        database_id=database_id,
        filter=filters,
        sorts=[{"property": "Date", "direction": "ascending"}]
    )

    matches = []
    for result in response["results"]:
        props = result["properties"]
        name = props["Name"]["title"][0]["text"]["content"]
        league = props["League"]["select"]["name"]
        iso_time = props["Date"]["date"]["start"]
        dt = datetime.fromisoformat(iso_time)
        readable_date = dt.strftime("%A, %b %d @ %I:%M %p")

        matches.append({
            "name": name,
            "league": league,
            "date": readable_date
        })

    return matches