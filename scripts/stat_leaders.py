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

year = 2025
categories = [
    "STROKES_GAINED",
    "OFF_TEE",
    "APPROACH_GREEN",
    "AROUND_GREEN",
    "PUTTING",
    "SCORING"
]

stat_leaders_list = []

for category in categories:
    query = {
        "operationName": "statLeaders",
        "variables": {
            "tourCode": "R",
            "year": year,  
            "category": category
        },
        "query": """
            query statLeaders($tourCode: TourCode!, $year: Int!, $category: StatCategory!) {
                statLeaders(tourCode: $tourCode, year: $year, category: $category) {
                    statCategory
                    categoryHeader
                    displayYear
                    subCategories {
                        subCategoryName
                        stats {
                            statId
                            playerId
                            playerName
                            statTitle
                            statValue
                            rank
                            country
                            countryFlag
                        }
                    }
                }
            }
        """
    }

    response = requests.post(url, headers=headers, json=query)
    response.raise_for_status()
    data = response.json()
    print(data)

    stat_data = data.get("data", {}).get("statLeaders", {})

    for subcat in stat_data.get("subCategories", []):
        subcat_name = subcat.get("subCategoryName", "")
        for stat in subcat.get("stats", []):
            stat_leaders_list.append({
                "year": stat_data.get("displayYear"),
                "category": stat_data.get("statCategory"),
                "sub_category": subcat_name,
                "stat_id": stat.get("statId"),
                "player_id": stat.get("playerId"),
                "player_name": stat.get("playerName"),
                "stat_title": stat.get("statTitle"),
                "stat_value": stat.get("statValue"),
                "rank": stat.get("rank"),
                "country": stat.get("country"),
            })

df = pd.DataFrame(stat_leaders_list)
df.to_csv("stat_leaders_2025.csv", index=False)
print("Saved to stat_leaders_2025.csv")
