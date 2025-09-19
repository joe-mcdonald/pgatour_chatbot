import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import requests
import sys
import re

client = chromadb.PersistentClient(path="./chroma_db")

embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")


def normalize_text(text):
    text = text.lower()
    text = re.sub(r'\bsg\b', 'strokes gained', text)
    text = re.sub(r'[\-_:]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_focus_stat(question):
    stat_map = {
        "putter": "putting",
        "putting": "putting",
        "off the tee": "off-the-tee",
        "driving": "driving",
        "approach": "approach",
        "scrambling": "scrambling",
        "around the green": "around-the-green",
        "tee to green": "tee-to-green"
    }
    for key, value in stat_map.items():
        if key in question.lower():
            return value
    return None

def is_rank_question(question):
    keywords = ["best", "top", "rank 1", "number one", "who leads", "leader", "highest ranked"]
    return any(kw in question.lower() for kw in keywords)

def query_chroma(question):
    normalized_question = normalize_text(question)
    all_results = []

    for name in ["pgatour_players_details", "golf_player_stats", "stats_leaders", "individual_tournament_results"]:
        try:
            collection = client.get_collection(name=name, embedding_function=embedding_function)
            results = collection.query(
                query_texts=[normalized_question],
                n_results=10,
            )
            if results and results["documents"][0]:
                all_results.extend(results["documents"][0])
        except Exception as e:
            print(f"Failed querying '{name}': {e}")

    if not all_results:
        return ["(No relevant context found)"]

    top_context = "\n\n".join(all_results)

    if is_rank_question(question):
        stat_focus = extract_focus_stat(question)
        rank_1_lines = [
            line for line in top_context.split("\n")
            if re.search(r"rank(ed)?\s*1\b", line.lower()) and (stat_focus in line.lower() if stat_focus else True)
        ]
        if rank_1_lines:
            return rank_1_lines[:5]  # Return top 3 lines with rank 1

    return top_context.split("\n")

    # return top_context.split("\n") if top_context else []



def ask_llm(prompt, context):
    full_prompt = f"""
You are a PGA Tour stats expert. You will only answer based on the provided context. Never invent stats, rankings, or values. If the context has stats, summarize them precisely, including player name, year, stat title, value, rank, and comparisons if available.

When providing answers:
- Include the player's stat value and rank, if available.
- Explain what the stat means (e.g. :"above average", "top 10%", "well below average") if possible.
- Keep it brief but informative.
- Use natural phrasing and avoid repeating the exact stat title unless helpful.
- If rank is missing, say so.
- If no relevant stat is present, respond clearly that the data isn't available.
- If asked for the best/leader in a stat, return the player ranked #1 based on the context.
- If asked for the best putter, driver, or approach player (and so on), return the player ranked #1 for strokes gained in that specific stat.
- If comparing players, mention differences in their stats.

Context:
{context}

Question:
{prompt}

Instructions:
Only answer based on the context above. Include rankings and values where available. Do not make up percentages or values not in the context.

Answer:"""

    res = requests.post(
        "http://localhost:11434/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "gpt-oss:latest",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that will answer questions based on the provided data."},
                {"role": "user", "content": full_prompt}
            ],
        }
    )
    return res.json()["choices"][0]["message"]["content"]



def main():
    user_question = sys.argv[1] if len(sys.argv) > 1 else input("Enter your question: ")
    context_docs = query_chroma(user_question)
    
    context_text = "\n".join(context_docs)
    # print(context_text if context_text.strip() else "(No relevant context found)\n")
    answer = ask_llm(user_question, context_text)
    print(f"Answer: {answer}")
    print("Done.")
    sys.exit(0)

if __name__ == "__main__":
    main()