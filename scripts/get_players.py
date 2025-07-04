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

def get_player_directory():
    # get all players:
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
    data = response.json()
    players = data.get("data", {}).get("playerDirectory", {}).get("players", [])
    return players


def get_player_details(player_id):
    query = {
        "operationName": "player",
        "variables": {"id": player_id},
        "query": """
            query player($id: ID!) {
              player(id: $id) {
                id
                displayName
                country
                countryFlag
                firstName
                lastName
                rank {
                  rank
                  statName
                }
                owgr
                bioLink
                playerBio {
                  age
                  born
                  family
                  heightMeters
                  weightImperial
                  playsFrom {
                    city
                    state
                  }
                  school
                  degree
                  social {
                    type
                    url
                  }
                  turnedPro
                }
              }
            }
        """
    }
    response = requests.post(url, headers=headers, json=query)
    response.raise_for_status()

    data = response.json()
    # print(data)
    
    return data.get("data", {}).get("player", {})



def main():
    players = get_player_directory()
    enriched = []
    # players = players[240:260]  # Uncomment for testing with a smaller subset
    for i, p in enumerate(players):
        # Skip inactive players:
        # if not p.get("isActive"):
        #     continue

        try:
            details = get_player_details(p["id"])
            bio = details.get("playerBio", {})
            residence = bio.get("playsFrom", {})


            enriched.append({
                "id": details.get("id"),
                "name": details.get("displayName"),
                "firstName": details.get("firstName"),
                "lastName": details.get("lastName") or "",
                "age": bio.get("age") or "",
                "born": bio.get("born") or "",
                "country": details.get("country") or "",
                "residence-city": residence.get("city"),
                "residence-state": residence.get("state"),
                "family": bio.get("family") or "",
                "school": bio.get("school") or "",
                "degree": bio.get("degree") or "",
                "graduation-year": bio.get("graduationYear") or "",
                "height": bio.get("heightMeters") or "",
                "weight": bio.get("weightImperial") or "",
                "turnedPro": bio.get("turnedPro") or "",
                "owgr": details.get("owgr") or "",
                "fedex_rank": details.get("rank").get("rank") if details.get("rank") else "",
                "fedex_stat": details.get("rank").get("statName") if details.get("rank") else "",
            })
            time.sleep(0.1)  # Add delay to avoid overloading the API

        except Exception as e:
            print(f"Error with {p['displayName']} ({p['id']}): {e}")
            print("\n\n")

    df = pd.DataFrame(enriched)
    df.to_csv("player_directory_enriched.csv", index=False)
    print(f"Saved {len(df)} enriched players to player_directory_enriched.csv")

if __name__ == "__main__":
    main()










# # response = requests.post(url, headers=headers, json=query)
# data = response.json()
# # print(data)  # Print first player for debugging


# players = data.get("data", {}).get("playerDirectory", {}).get("players", [])

# # get all ids:
# player_ids = [player.get("id") for player in players]


# rows = []
# for player in players:
#     player_bio = player.get("playerBio", {})
#     rows.append({
#         "id": player.get("id"),
#         "isActive": player.get("isActive"),
#         "firstName": player.get("firstName"),
#         "lastName": player.get("lastName"),
#         "shortName": player.get("shortName"),
#         "displayName": player.get("displayName"),
#         "alphaSort": player.get("alphaSort"),
#         "country": player.get("country"),
#         "countryFlag": player.get("countryFlag"),
#         "age": player_bio.get("age"),
#         "education": player_bio.get("education"),
#         "turnedPro": player_bio.get("turnedPro")
#     })


# df = pd.DataFrame(rows)
# df.to_csv("./players.csv", index=False)
# print("Saved player data to players.csv")