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
    # Define list of classes (can make this dynamic later)
    class_options=("All" "Cloud Computing & Security" "Advanced Computer Architecture" "Game Design" "Computing Beyond CPUs")

    class_selection=$(printf "%s\n" "${class_options[@]}" | fzf --prompt="Select class (or All): ")

    if [[ -z "$class_selection" ]]; then
      echo "❌ No class selected. Exiting."
      exit 1
    fi

    if [[ "$class_selection" == "All" ]]; then
      python3 ~/notion-client/query_assignments.py
    else
      python3 ~/notion-client/query_assignments.py --class "$class_selection"
    fi
    ;;


  *)
    echo "❌ Invalid selection. Exiting."
    exit 1
    ;;
esac
