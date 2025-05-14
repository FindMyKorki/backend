#!/bin/bash

ENV_FILE="/app/.env"  # not /app/.env
KEY="BACKEND_URL"
TIMEOUT=30

echo "[⏳] Waiting for $KEY to be updated in $ENV_FILE..."

for i in $(seq 1 $TIMEOUT); do
    if grep "^$KEY=http" "$ENV_FILE" > /dev/null; then
        echo "[✅] Found updated $KEY in $ENV_FILE"
        break
    fi
    echo "  ... still waiting ($i/$TIMEOUT)"
    sleep 1
done


echo "[⚙️] Sourcing $ENV_FILE to update environment variables..."
# This will load the variables from the .env file into the shell environment.
set -a && . "$ENV_FILE" && set +a

echo "[🚀] Starting FastAPI server on port ${BACKEND_PORT}..."
exec uvicorn main:app --host 0.0.0.0 --port "${BACKEND_PORT}" --reload