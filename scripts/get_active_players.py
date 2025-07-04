import requests
import pandas as pd
import time

url = "https://orchestrator.pgatour.com/graphql"
headers = {
    "x-api-key": "da2-gsrx5bibzbb4njvhl7t37wqyl4",
    "content-type": "application/json",
    "origin": "https://www.pgatour.com",
    "referer": "https://www.pgatour.com"
}

query = {
    "operationName": "playerDirectory",
        "variables": {
            "tourCode": "R",
        },
        "query": """
            query playerDirectory($tourCode: TourCode!) {
                playerDirectory(tourCode: $tourCode) {
                    tourCode
                    players {
                        id
                        isActive
                        firstName
                        lastName
                        shortName
                        displayName
                        alphaSort
                        country
                        countryFlag
                        headshot
                        playerBio {
                            id
                            age
                            education
                            turnedPro
                        }
                    }
                }
            }
        """
}

response = requests.post(url, headers=headers, json=query)
response.raise_for_status()

data = response.json()

players = data.get("data", {}).get("playerDirectory", {})


active_players = []
for player in players.get("players", []):
    if player.get("isActive") == True:
        active_players.append(player)

active_players_df = pd.DataFrame(active_players)

player_list = []
# create a csv with columns for id, name, and link:
for player in active_players:
    player_list.append({
        "id": player.get("id"),
        "name": player.get("displayName"),
        "link": f"https://www.pgatour.com/player/{player.get('id')}/{player.get('firstName').lower().replace(' ', '-')}-{player.get('lastName').lower().replace(' ', '-')}/",
    })

active_players_df = pd.DataFrame(player_list)
# Save the DataFrame to a CSV file
active_players_df.to_csv("active_players.csv", index=False)
