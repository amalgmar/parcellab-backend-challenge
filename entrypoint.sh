#!/bin/bash
set -e

echo "✅ Starting FastAPI app..."
exec uvicorn app.main:app --host "$API_HOST" --port "$API_PORT" --log-level "debug"