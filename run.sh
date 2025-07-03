python3 -m venv chroma_env

source chroma_env/bin/activate

pip install -r requirements.txt
pip install chromadb[server]

chroma run --path ./chroma_db