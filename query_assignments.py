import argparse
from datetime import datetime, timedelta
from notion_assignments import fetch_this_weeks_assignments, add_status_to_assignments, group_assignments_by_class
from notion_client import Client
import os

def main():
    parser = argparse.ArgumentParser(description="Query Notion school assignments.")
    parser.add_argument("--class", dest="class_filter", help="Filter by class (Project name)")
    parser.add_argument("--week", action="store_true", help="Only show assignments due this week")
    args = parser.parse_args()

    today = datetime.today()
    print_str = f"\n📅 Assignments Due"
    if args.week:
        print_str += " This Week"
    else:
        print_str += f" (from {today.strftime('%Y-%m-%d')})"
    print(print_str + ":\n")

    # Initialize Notion client manually to access raw results (for status)
    notion = Client(auth=os.environ["NOTION_API_TOKEN"])
    database_id = "a54c41eb884442f18cc221c0febbeee0"

    # Construct filters
    filters = [
        {"property": "Area", "select": {"equals": "School"}}
    ]

    if args.week:
        filters.append({
            "property": "Due Date",
            "date": {
                "this_week": {}
            }
        })
    else:
        filters.append({
            "property": "Due Date",
            "date": {
                "on_or_after": today.strftime("%Y-%m-%d")
            }
        })

    response = notion.databases.query(
        database_id=database_id,
        filter={"and": filters},
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
    
    if args.class_filter:
        # Filter by class name (case-insensitive match)
        class_name = args.class_filter.lower()
        filtered = [a for a in assignments if a["project"].lower() == class_name]

        if not filtered:
            print(f"❌ No assignments found for class '{args.class_filter}'.")
            return

        from tabulate import tabulate
        print(f"📚 {args.class_filter}\n")
        table_data = [(a['name'], a['due'], a['status_str']) for a in filtered]
        headers = ["Name", "Due Date", "Status"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    else:
        group_assignments_by_class(assignments)


if __name__ == "__main__":
    main()

