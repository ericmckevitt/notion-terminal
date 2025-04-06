import argparse
from datetime import datetime
from notion_assignments import fetch_this_weeks_assignments, add_status_to_assignments, group_assignments_by_class
from notion_client import Client
import os

def main():
    parser = argparse.ArgumentParser(description="Query Notion school assignments.")
    # In the future, you could add more flags here like:
    # parser.add_argument("--flat", action="store_true", help="Show flat table instead of grouped")
    args = parser.parse_args()

    today = datetime.today().strftime("%Y-%m-%d")
    print(f"\n📅 Assignments Due (from {today}):\n")

    # Initialize Notion client manually to access raw results (for status)
    notion = Client(auth=os.environ["NOTION_API_TOKEN"])
    database_id = "a54c41eb884442f18cc221c0febbeee0"

    filters = {
        "and": [
            {"property": "Area", "select": {"equals": "School"}},
            {"property": "Due Date", "date": {"on_or_after": today}}
        ]
    }

    response = notion.databases.query(
        database_id=database_id,
        filter=filters,
        sorts=[{"property": "Due Date", "direction": "ascending"}]
    )

    raw_results = response["results"]
    if not raw_results:
        print("🎉 No more assignments!")
        return

    # Convert to assignment list
    assignments = []
    for result in raw_results:
        props = result["properties"]
        name = props["Name"]["title"][0]["text"]["content"]
        due_date = props["Due Date"]["date"]["start"]
        dt = datetime.fromisoformat(due_date)
        readable_date = dt.strftime("%A, %b %d")
        project = props["Project"]["select"]["name"] if props["Project"]["select"] else "-"
        assignments.append({
            "name": name,
            "due": readable_date,
            "project": project
        })

    add_status_to_assignments(assignments, raw_results)
    group_assignments_by_class(assignments)

if __name__ == "__main__":
    main()
