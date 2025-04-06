from notion_client import Client
from datetime import datetime, timedelta
import os

def fetch_this_weeks_assignments():
    notion = Client(auth=os.environ["NOTION_API_TOKEN"])
    # https://www.notion.so/ericmckevitt/a54c41eb884442f18cc221c0febbeee0?v=75840accf78347a1b1e443cac54a5ae5&pvs=4
    database_id = "a54c41eb884442f18cc221c0febbeee0"

    today = datetime.today().strftime("%Y-%m-%d")

    filters = {
        "and": [
            {
                "property": "Area",
                "select": {"equals": "School"}
            },
            {
                "property": "Due Date",
                "date": {
                    "on_or_after": today,
                }
            }
        ]
    }

    response = notion.databases.query(
        database_id=database_id,
        filter=filters,
        sorts=[{"property": "Due Date", "direction": "ascending"}]
    )

    assignments = []
    for result in response["results"]:
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

    return assignments

if __name__ == "__main__":
    from tabulate import tabulate

    assignments = fetch_this_weeks_assignments()
    print(assignments)

    table_data = [(a['name'], a['project'], a['due']) for a in assignments]
    headers = ["Name", "Class", "Due Date"]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))