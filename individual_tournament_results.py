import requests
import pandas as pd

url = "https://orchestrator.pgatour.com/graphql"
headers = {
    "x-api-key": "da2-gsrx5bibzbb4njvhl7t37wqyl4",
    "content-type": "application/json",
    "origin": "https://www.pgatour.com",
    "referer": "https://www.pgatour.com"
}

for year in range(2012, 2026):
    for tournament in all_ids_by_year[year]:
        tournament_id = tournament["id"]
        tournament_name = tournament["name"]
        query = {
            "operationName": "TournamentPastResults",
            "variables": {
                "id": tournament_id
            },
            "query": """
            query TournamentPastResults($id: ID!) {
            tournamentPastResults(id: $id) {
                id
                players {
                position
                player {
                    displayName
                }
                rounds {
                    score
                }
                total
                parRelativeScore
                additionalData
                }
            }
            }
            """
        }

        response = requests.post(url, headers=headers, json=query)
        data = response.json()

        rows = []
        for p in data["data"]["tournamentPastResults"]["players"]:
            name = p["player"]["displayName"]
            rounds = [r["score"] for r in p["rounds"]]
            rows.append({
                "Player": name,
                "Position": p["position"],
                "R1": rounds[0] if len(rounds) > 0 else "",
                "R2": rounds[1] if len(rounds) > 1 else "",
                "R3": rounds[2] if len(rounds) > 2 else "",
                "R4": rounds[3] if len(rounds) > 3 else "",
                "Total": p["total"],
                "To Par": p["parRelativeScore"],
                "Money": p["additionalData"][1] if len(p["additionalData"]) > 1 else ""
            })

        df = pd.DataFrame(rows)

        # Save to CSV
        df.to_csv(f"./individual_tournament_results/{year}/{year}_{tournament_name}.csv")


