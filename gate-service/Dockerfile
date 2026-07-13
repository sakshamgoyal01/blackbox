FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install OPA
RUN wget -O /usr/local/bin/opa \
    https://openpolicyagent.org/downloads/latest/opa_linux_amd64_static && \
    chmod +x /usr/local/bin/opa

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create non-root user
RUN groupadd --system appgroup && \
    useradd --system --gid appgroup --create-home appuser

# Give ownership to application user
RUN chown -R appuser:appgroup /app

# Run application as non-root
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
