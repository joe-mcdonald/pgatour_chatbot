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
    

    df = pd.DataFrame(tournaments)

    # Save to CSV
    df.to_csv(f"./tournament_results/tournament_results_{year}.csv", index=False)

    print(f"Saved tournament results from {year} to CSV.")