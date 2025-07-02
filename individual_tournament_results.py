import requests
import pandas as pd

url = "https://orchestrator.pgatour.com/graphql"
headers = {
    "x-api-key": "da2-gsrx5bibzbb4njvhl7t37wqyl4",
    "content-type": "application/json",
    "origin": "https://www.pgatour.com",
    "referer": "https://www.pgatour.com"
}

all_ids_by_year = {}

for year in range(2012, 2026):
    query = {
        "operationName": "Schedule",
        "variables": {
            "tourCode": "R",
            "year": f"{year}"
        },
        "query": """
        query Schedule($tourCode: String!, $year: String!) {
            schedule(tourCode: $tourCode, year: $year) {
            completed {
            month
            tournaments {
                tournamentName
                id
                champion
                championId
                championEarnings
                startDate
            }
            }
        }
        }
        """
    }

    response = requests.post(url, headers=headers, json=query)
    data = response.json()

    tournaments = []


    try:
        for month in data["data"]["schedule"]["completed"]:
            for t in month["tournaments"]:
                # Store tournament IDs for this year
                all_ids_by_year[year] = [{"id": t["ID"], "name": t["Tournament"]} for t in tournaments]
                tournaments.append({
                    "Tournament": t.get("tournamentName"),
                    "ID": t.get("id"),
                    "Champion": t.get("champion"),
                    "Champion ID": t.get("championId"),
                    "Earnings": t.get("championEarnings"),
                    "Start Date": pd.to_datetime(t.get("startDate"), unit="ms").date() if t.get("startDate") else None
                })
    except Exception as e:
        print(f"Error parsing data: {e}")

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


