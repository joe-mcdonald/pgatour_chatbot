import pandas as pd
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import sys
import os
import re
import glob

def normalize_text(text):
    text = text.lower()
    text = re.sub(r'\bsg\b', 'strokes gained', text)
    text = re.sub(r'[\-_:]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


persist_dir = "./chroma_db"
client = chromadb.PersistentClient(path=persist_dir)
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")


def process_golf_player_details():
    player_details_collection = client.get_or_create_collection(
        name="pgatour_players_details",
        embedding_function=embedding_fn
    )

    df = pd.read_csv("player_directory_enriched.csv")
    print("Adding golf player details...")

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
                doc += f" They attended {row['school']}."
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
            player_details_collection.add(
                ids = [str(row['id'])],
                documents = [doc],
                metadatas = [metadata],
            )
            print(f"\rProcessing details for {name}", end='', flush=True)
        except Exception as e:
            print(f"Error processing row {row['id']}: {e}")


def process_golf_player_stats():
    print("Now adding golf player stats...")

    stats_collection = client.get_or_create_collection(
        name="golf_player_stats",
        embedding_function=embedding_fn
    )

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
                    stat_title = normalize_text(row.get('Stat Title', ''))
                    value = row.get('Value', '')
                    rank = row.get('Rank', '')
                    supporting_stat = row.get('Supporting Stat', '')
                    supporting_value = row.get('Supporting Value', '')

                    if pd.notna(stat_title) and pd.notna(value):
                        print(f"\rProcessing {player_name} - Stat {i+1}: {stat_title} ({value})", end='', flush=True)
                        stat_title = stat_title.strip().capitalize()

                        try:
                            value = round(float(value), 3)
                        except:
                            pass # ignore if conversion fails

                        if pd.notna(rank) and str(rank).strip() not in ["-", "--", ""]:
                            try:
                                rank_int = int(float(rank))
                                doc_test = (
                                    f"In the 2025 PGA Tour season, {player_name} ranked {rank_int} "
                                    f"in '{stat_title}' with a value of {value}."
                                )
                            except:
                                doc_test = (
                                    f"In the 2025 PGA Tour season, {player_name} recorded a value of {value} "
                                    f"in '{stat_title}', but no valid rank was available."
                                )
                        else:
                            doc_test = (
                                f"In the 2025 PGA Tour season, {player_name} recorded a value of {value} "
                                f"in '{stat_title}', but no rank was available."
                            )

                        if pd.notna(supporting_stat) and pd.notna(supporting_value):
                            doc_test += f" The supporting stat '{supporting_stat}' was {supporting_value}."
                    else:
                        doc_test = f"{player_name} has a stat entry for '{stat_title}'."

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


def process_stat_leaders():
    print("adding stat leaders...")

    stat_leader_path = "stat_leaders_2025.csv"

    stats_leaders_collection = client.get_or_create_collection(
        name="stats_leaders",
        embedding_function=embedding_fn
    )

    if os.path.exists(stat_leader_path):
        df_leaders = pd.read_csv(stat_leader_path)

        stat_docs = []
        stat_ids = []

        for i, row in df_leaders.iterrows():
            year = row["year"]
            player = row["player_name"]
            stat_title = row["stat_title"]
            stat_value = row["stat_value"]
            rank = row["rank"]
            country = row["country"]
            category = row["category"]
            subcat = row["sub_category"]

            # Natural language summary
            doc = (
                f"In the {year} PGA Tour season, {player} ranked {rank} in '{stat_title}' "
                f"with a value of {stat_value}. This stat falls under the '{subcat}' sub-category "
                f"of the '{category}' category. {player} represents {country}."
            )

            print(f"\rProcessing details for the stat leader for {stat_title}", end='', flush=True)
            stat_docs.append(doc)
            stat_ids.append(f"stat_leader_{i}")

        # Add to existing ChromaDB collection
        stats_leaders_collection.add(
            documents=stat_docs,
            ids=stat_ids,
        )

        print(f"Added {len(stat_docs)} stat leader records to golf_player_stats.")
    else:
        print("stat_leaders_2025.csv not found. Skipping stat leader ingestion.")


def process_tournament_csvs(data_dir="./individual_tournament_results"):
    print("Now adding individual tournament results...")

    tournament_collections = client.get_or_create_collection(
        name="individual_tournament_results",
        embedding_function=embedding_fn
    )
    csv_files = glob.glob(os.path.join(data_dir, "**/*.csv"), recursive=True)
    documents = []
    ids = []

    for file_path in csv_files:
        try:
            df = pd.read_csv(file_path)
            if df.empty or "Player" not in df.columns:
                continue

            year = os.path.basename(os.path.dirname(file_path))
            tournament = os.path.splitext(os.path.basename(file_path))[0].replace("_", " ")

            for idx, row in df.iterrows():
                name = row["Player"]
                pos = row.get("Position", "N/A")
                score = row.get("To Par", row.get("score", "N/A"))
                money = row.get("Money", "N/A")
                doc = f"In the {tournament}, {name} finished {pos} with a total score of {score}. They earned ${money}."
                documents.append(doc)
                unique_id = f"{tournament}_{name.replace(' ', '_')}_{idx}"
                ids.append(unique_id)
            print(f"\rProcessing details for the event {unique_id}", end='', flush=True)

        except Exception as e:
            print(f"Skipping file {file_path} due to error: {e}")
    
    if documents:
        BATCH_SIZE = 5000
        for doc_batch, id_batch in zip(chunks(documents, BATCH_SIZE), chunks(ids, BATCH_SIZE)):
            tournament_collections.add(documents=doc_batch, ids=id_batch)

        # print(f"Added {len(documents)} tournament results to individual_tournament_results.")

process_golf_player_details()
process_golf_player_stats()
process_stat_leaders()
process_tournament_csvs()

print()
print(f"ChromaDB setup complete and data persisted with  entries.")
