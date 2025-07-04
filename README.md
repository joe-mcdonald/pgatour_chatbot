# PGA Tour Data and Stats Chatbot!

This project is a chatbot that uses live data from the PGA Tour's website. There is a Docker container that scrapes the data using GraphQL queries for the following information:

- Individual player details (birth date, country, when they turned pro, etc.)
- Individual player stats (strokes gained, GIR%, par 4 scoring average, etc.)
- Full results from each tournament from 2012-present, including the money won by each player
- Full list of all active and past PGA Tour golfers

All this data is stored in CSV files and processed into a ChromaDB vector database for the chatbot. The database is updated by building and running the 
```
docker build -t pgatour-updater .

docker run \
  -v "$PWD":/app \
  -v ~/.ssh:/root/.ssh \
  pgatour-updater
```

No need to install any dependencies (this is done within the docker container environment), but running ```pip3 install -r requirements.txt``` is recommended.

To use the chatbot, which uses Mistral Nemo, run ```python3 scripts/gradio_app.py``` and navigate to `http://127.0.0.1:7860/`