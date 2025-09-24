FROM python:3.11-slim

# Evita pyc y buffers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crea usuario no-root
RUN useradd -ms /bin/bash appuser

WORKDIR /app

# Dependencias del sistema (wget para healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
  && rm -rf /var/lib/apt/lists/*

# Instala dependencias de Python
# Si tienes requirements.txt, copia e instala aquí
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código
COPY app ./app

# Puerto por defecto (configurable)
ENV PORT=8000
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget -qO- http://127.0.0.1:${PORT}/health || exit 1

USER appuser

# Arranque: Uvicorn con reload deshabilitado (prod)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]