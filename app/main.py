from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routers import client, purchase

app = FastAPI(title="API VISE (Python + FastAPI)")

@app.get("/health", tags=["health"])
def health():
    return JSONResponse({"ok": True}, headers={"Cache-Control": "no-store"})

app.include_router(client.router)
app.include_router(purchase.router)