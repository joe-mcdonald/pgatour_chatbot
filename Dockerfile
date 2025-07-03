# Dockerfile
FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Ensure SSH works inside the container for pushing to GitHub
RUN apt-get update && apt-get install -y openssh-client git && \
    mkdir -p /root/.ssh && \
    ssh-keyscan github.com >> /root/.ssh/known_hosts

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["bash", "run_all.sh"]