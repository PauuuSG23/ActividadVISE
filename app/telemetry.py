import os
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor


def init_tracing(app):
    """Configura SOLO TRACES usando OpenTelemetry y Axiom."""

    token = os.getenv("AXIOM_TOKEN")
    domain = os.getenv("AXIOM_DOMAIN", "api.axiom.co")
    dataset = os.getenv("AXIOM_DATASET")

    if not (token and dataset):
        print("AXIOM tracing not configured. Missing env vars.")
        return

    resource = Resource.create({
        "service.name": "python-fastapi-api",
        "service.environment": "prod"
    })

    # Configurar proveedor de trazas
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    # Exportador OTLP hacia Axiom
    exporter = OTLPSpanExporter(
        endpoint=f"https://{domain}/v1/traces",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Axiom-Dataset": dataset
        }
    )

    tracer_provider.add_span_processor(BatchSpanProcessor(exporter))

    # Auto-instrumentación
    FastAPIInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()
