#!/bin/bash
set -e  # exit if any command fails

echo "Running PGA Tour update scripts..."
echo "running get_active_players.py"
# python3 scripts/get_active_players.py

echo "running tournament_results.py"
# python3 scripts/tournament_results.py

echo "running individual_tournament_results.py"
# python3 scripts/individual_tournament_results.py

echo "running player_individual_stats.py"
# python3 scripts/player_individual_stats.py

echo "running get_players.py"
# python3 scripts/get_players.py

echo "Done with PGA Tour update scripts."

echo "Setting up ChromaDB, this may take a while..."
# python3 scripts/chroma_setup.py

echo "Committing and pushing to GitHub..."
git config --global user.name "joe-mcdonald"
git config --global user.email "joemcd0224@gmail.com"

git add .
git commit -m "Auto commit from Docker container" || echo "No changes to commit."

git pull origin main --rebase || echo "Rebase not required."

# git add .
# git commit -m "Automated update from Docker container" || echo "No changes to commit after rebase."
# git push git@github.com:joe-mcdonald/pgatour_chatbot.git HEAD:main
git push origin main

# git pull origin main

git diff --quiet || git status

echo "All scripts executed successfully and changes pushed to GitHub."