from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routers.client import router as client_router
from app.routers.purchase import router as purchase_router

# OpenTelemetry initialization
try:
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    # requests instrumentation is optional; if unavailable, skip
    try:
        from opentelemetry.instrumentation.requests import RequestsInstrumentor
        _requests_instrumentation_available = True
    except Exception:
        _requests_instrumentation_available = False

    # Create a resource describing this service
    resource = Resource.create({"service.name": "api-vise"})

    # Configure tracer provider
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    # Add a simple Console exporter for local development / tests
    console_exporter = ConsoleSpanExporter()
    span_processor = BatchSpanProcessor(console_exporter)
    tracer_provider.add_span_processor(span_processor)

    app = FastAPI(title="API VISE (Python + FastAPI)")

    # Instrument FastAPI and requests (auto-instrumentation)
    try:
        FastAPIInstrumentor().instrument_app(app)
    except Exception:
        # if instrument_app fails (e.g., during tests), continue without crashing
        pass
    if _requests_instrumentation_available:
        try:
            RequestsInstrumentor().instrument()
        except Exception:
            pass
except Exception:
    # If OpenTelemetry packages are not installed, create the app normally.
    app = FastAPI(title="API VISE (Python + FastAPI)")

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