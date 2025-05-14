FROM python:3.12-slim
RUN apt-get update
ENV PYTHONPATH=/app/app
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y docker.io
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", --reload]