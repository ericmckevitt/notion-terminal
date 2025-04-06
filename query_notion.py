from notion_client import Client
import os
from datetime import datetime, timezone

notion = Client(auth=os.environ["NOTION_API_TOKEN"])
database_id = "d78e531fc51a4f3b870f9773d6b0ee85"

today = datetime.today().strftime("%Y-%m-%d")

response = notion.databases.query(
    database_id=database_id,
    filter={
        "property": "Date",
        "date": {
            "on_or_after": today
        }
    },
    sorts=[
        {
            "property": "Date",
            "direction": "ascending"
        }
    ]
)

# Print nicely
print(f"\n📅 Upcoming Matches (from {today}):\n")

for result in response["results"]:
    props = result["properties"]
    name = props["Name"]["title"][0]["text"]["content"]
    league = props["League"]["select"]["name"]
    iso_time = props["Date"]["date"]["start"]

    # Convert ISO string to readable format
    dt = datetime.fromisoformat(iso_time)
    readable_date = dt.strftime("%A, %b %d @ %I:%M %p")

    print(f"⚽ {name}")
    print(f"   🏆 {league}")
    print(f"   🕒 {readable_date}\n")
