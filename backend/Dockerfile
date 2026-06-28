FROM python:3.12-slim

LABEL org.opencontainers.image.title="ProtonFix Backend"
LABEL org.opencontainers.image.description="Deterministic Linux gaming log diagnosis engine — FastAPI backend"

WORKDIR /app

# Install dependencies first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# /data is mounted as a named volume at runtime for persistence.
# Set here so the directory exists if someone runs the image without a volume.
ENV PROTONFIX_DATA_DIR=/data
RUN mkdir -p /data

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
