from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routers.client import router as client_router
from app.routers.purchase import router as purchase_router
# importa los routers concretos (evita ambigüedades)
from app.routers.client import router as client_router
from app.routers.purchase import router as purchase_router
from app.telemetry import init_tracing


app = FastAPI(title="API VISE (Python + FastAPI)")

try:
    init_tracing(app)
except Exception as e:
    print("Tracing init failed:", e)

# endpoint raíz solo para verificar que responde 200
@app.get("/", tags=["health"])
def root():
    return {"ok": True, "msg": "API VISE (FastAPI) online"}

# healthcheck
@app.get("/health", tags=["health"])
def health():
    return JSONResponse({"ok": True}, headers={"Cache-Control": "no-store"})

# monta routers
app.include_router(client_router)
app.include_router(purchase_router)