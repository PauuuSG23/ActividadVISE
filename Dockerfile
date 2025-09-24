FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# AÑADIR PYTHONPATH para resolver 'app.*'
ENV PYTHONPATH=/app

RUN useradd -ms /bin/bash appuser
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV PORT=8000
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget -qO- http://127.0.0.1:${PORT}/health || exit 1

USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]