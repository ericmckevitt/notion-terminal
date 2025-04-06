from notion_client import Client
from datetime import datetime, timedelta
import os
from tabulate import tabulate
from collections import defaultdict

def fetch_this_weeks_assignments():
    notion = Client(auth=os.environ["NOTION_API_TOKEN"])
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

def group_assignments_by_class(assignments):
    from collections import defaultdict
    grouped = defaultdict(list)

    for a in assignments:
        grouped[a['project']].append(a)

    for project, items in grouped.items():
        print(f"\n📚 {project}\n")
        table_data = [(a['name'], a['due'], a['status_str']) for a in items]
        headers = ["Name", "Due Date", "Status"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

def add_status_to_assignments(assignments, raw_results):
    """Mutates `assignments` to include 'status' and colorized 'status_str'"""
    for a, result in zip(assignments, raw_results):
        props = result["properties"]
        status = props.get("Status", {}).get("status", {}).get("name", "-")
        a["status"] = status
        a["status_str"] = colorize_status(status)

def colorize_status(status):
    color_map = {
        "Done": "\033[38;5;114m",         # Green
        "In progress": "\033[38;5;109m",  # Blue
        "Not started": "\033[38;5;204m",  # Red
    }
    color = color_map.get(status, "")
    reset = "\033[0m"
    return f"{color}{status}{reset}"

if __name__ == "__main__":
    notion = Client(auth=os.environ["NOTION_API_TOKEN"])
    database_id = "a54c41eb884442f18cc221c0febbeee0"
    
    # Get raw response so we can extract 'Status' before formatting
    today = datetime.today().strftime("%Y-%m-%d")
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

    # Format the assignments
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
