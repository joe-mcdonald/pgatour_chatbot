import pandas as pd
import chromadb
from chromadb.config import Settings
import os

persist_dir = "./chroma_db"
client = chromadb.PersistentClient(path=persist_dir)
collection = client.get_or_create_collection(name="pgatour_players_details")

df = pd.read_csv("player_directory_enriched.csv")

for _, row in df.iterrows():
    try:
        name = row['name']
        country = row['country']
        doc = f"{name} is a professional golfer"

        if pd.notna(country):
            doc += f" from {country}"
        if pd.notna(row.get('born')):
            doc += f", born on {row['born']}"
        doc += "."

        if pd.notna(row.get('turnedPro')):
            doc += f" Turned professional in {int(row['turnedPro'])}."
        if pd.notna(row.get('residence-city')) and pd.notna(row.get('residence-state')):
            doc += f" Resides in {row['residence-city']}, {row['residence-state']}."
        if pd.notna(row.get('family')):
            doc += f" Family: {row['family']}."
        if pd.notna(row.get('school')):
            doc += f" Attended {row['school']}."
        if pd.notna(row.get('degree')):
            doc += f" Degree in {row['degree']}."
        if pd.notna(row.get('height')):
            doc += f" Height: {row['height']} meters."
        if pd.notna(row.get('weight')):
            doc += f" Weight: {row['weight']} lbs."
        if pd.notna(row.get('owgr')):
            doc += f" Official World Golf Ranking (OWGR): {int(row['owgr'])}."
        if pd.notna(row.get('fedex_rank')) and pd.notna(row.get('fedex_stat')):
            doc += f" FedEx Rank: {int(row['fedex_rank'])} in {row['fedex_stat']}."

        metadata = row.dropna().to_dict()

        collection.add(
            ids = [str(row['id'])],
            documents = [doc],
            metadatas = [metadata],
        )
    except Exception as e:
        print(f"Error processing row {row['id']}: {e}")


print("Now adding golf player stats...")

stats_collection = client.get_or_create_collection(name="golf_player_stats")

stats_dir = "./golf_player_stats"

for filename in os.listdir(stats_dir):
    if filename.endswith(".csv"):
        filepath = os.path.join(stats_dir, filename)
        try:
            df = pd.read_csv(filepath)

            if df.empty or 'Stat Title' not in df.columns:
                print(f"Skipping empty or invalid file: {filename}")
                continue

            documents = []
            metadatas = []
            ids = []

            player_name = filename.replace("_stats_2025.csv", "").replace("-", " ").title()

            for i, row in df.iterrows():
                stat_title = row.get('Stat Title', '')
                value = row.get('Value', '')
                rank = row.get('Rank', '')
                supporting_stat = row.get('Supporting Stat', '')
                supporting_value = row.get('Supporting Value', '')

                doc_test = f"""
                Player: {player_name}
                Stat Title: {stat_title}
                Value: {value}
                Rank: {rank}
                Supporting Stat: {supporting_stat}
                Supporting Value: {supporting_value}
                """.strip().replace("\n", " ")

                documents.append(doc_test)
                ids.append(f"{player_name.replace(' ', '_')}_{i}")
                metadatas.append({
                    "player": player_name,
                    "stat_title": stat_title,
                    "value": value,
                    "rank": rank,
                    "supporting_stat": supporting_stat,
                    "supporting_value": supporting_value,
                })
            
            stats_collection.add(
                documents = documents,
                metadatas = metadatas,
                ids = ids,
            )
        except Exception as e:
            print(f"Error processing file {filename}: {e}")


print(f"ChromaDB setup complete and data persisted with {len(df)} entries.")
 