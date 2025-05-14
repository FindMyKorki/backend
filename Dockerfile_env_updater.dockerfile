FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y docker.io curl && \
    pip install requests

CMD ["python", "start_ngrok.py"]

COPY . /app