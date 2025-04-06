#!/bin/bash

# Step 1: Select the Notion database
options=(
  "🏟️  Football"
  "📚 Assignments"
)

db_selection=$(printf "%s\n" "${options[@]}" | fzf --prompt="Select Notion query: ")

if [[ -z "$db_selection" ]]; then
  echo "❌ No database selected. Exiting."
  exit 1
fi

# Step 2: Handle each database type
case "$db_selection" in
  "🏟️  Football")
    team_names=("Manchester City" "Real Madrid")
    team_flags=("mc" "rm")

    team_selection=$(printf "%s\n" "${team_names[@]}" | fzf --prompt="Select team: ")

    if [[ -z "$team_selection" ]]; then
      echo "❌ No team selected. Exiting."
      exit 1
    fi

    # Map team name to flag
    for i in "${!team_names[@]}"; do
      if [[ "${team_names[$i]}" == "$team_selection" ]]; then
        team_flag="${team_flags[$i]}"
        break
      fi
    done

    python3 ~/notion-client/query_football.py --team "$team_flag"
    ;;

  "📚 Assignments")
    python3 ~/notion-client/query_assignments.py
    ;;

  *)
    echo "❌ Invalid selection. Exiting."
    exit 1
    ;;
esac
