import requests
import pandas as pd

# Endpoint and headers
url = "https://orchestrator.pgatour.com/graphql"
headers = {
    "x-api-key": "da2-gsrx5bibzbb4njvhl7t37wqyl4",
    "content-type": "application/json",
    "origin": "https://www.pgatour.com",
    "referer": "https://www.pgatour.com"
}

# get links from active_players.csv
links = pd.read_csv("./active_players.csv")["link"].tolist()


players = {
    int(url.split("/")[4]): url.split("/")[5]
    for url in links
}

year = "2025"

for player_id, player_name in players.items():
  # GraphQL query
  query = {
      "operationName": "PlayerProfileStatsFullV2",
      "variables": {
          "playerId": player_id,
      },
      "query": """
      query PlayerProfileStatsFullV2($playerId: ID!) {
        playerProfileStatsFullV2(playerId: $playerId) {
          playerProfileStatsFull {
            stats {
              statId
              title
              value
              rank
              aboveOrBelow
              supportingStat {
                description
                value
              }
              supportingValue {
                description
                value
              }
            }
          }
        }
      }
      """
  }

  # Send request
  response = requests.post(url, headers=headers, json=query)
  data = response.json()

  try:
      stats_section = data.get("data", {}).get("playerProfileStatsFullV2", {})
      stats_list = stats_section.get("playerProfileStatsFull")

      if not stats_list or not isinstance(stats_list, list):
          raise ValueError("Missing or invalid 'playerProfileStatsFull'")

      stats = stats_list[0].get("stats", [])
  except Exception as e:
      print(f"Failed to extract stats: {e}")
      stats = []

  if stats:
      df = pd.DataFrame([{
          "Stat Title": s.get("title"),
          "Value": s.get("value"),
          "Rank": s.get("rank"),
          "Above/Below": s.get("aboveOrBelow", ""),
          "Supporting Stat": f"{s['supportingStat']['description']}: {s['supportingStat']['value']}" if s.get("supportingStat") else "",
          "Supporting Value": f"{s['supportingValue']['description']}: {s['supportingValue']['value']}" if s.get("supportingValue") else ""
      } for s in stats])

      pd.set_option("display.max_rows", None)
      pd.set_option("display.max_columns", None)
      pd.set_option("display.width", None)
      pd.set_option("display.max_colwidth", None)

      # Optional: save to CSV
      df.to_csv(f"./golf_player_stats/{player_name}_stats_{year}.csv", index=False)
  else:
      print("No stats found.")
