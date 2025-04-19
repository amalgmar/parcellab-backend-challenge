from fastapi import FastAPI
from app.api.routes import shipments

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(shipments.router)
