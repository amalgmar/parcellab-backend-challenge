#!/bin/bash
set -e

echo "🔧 Checking and running Alembic migrations..."

if ! alembic current &>/dev/null; then
    echo "📌 No Alembic history — stamping DB..."
    alembic stamp head
fi

alembic upgrade head
echo "✅ Migrations applied."

echo "🌱 Seeding sample data..."
python -m app.scripts.seed

echo "🚀 Starting FastAPI app..."
exec uvicorn app.main:app --host "$API_HOST" --port "$API_PORT" --reload --log-level "debug"
