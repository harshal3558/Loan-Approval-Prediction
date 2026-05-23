
# =========================
# 1️⃣ Builder stage – install build‑time deps
# =========================
FROM python:3.10-slim AS builder

# System dependencies required for building wheels (numpy, pandas, scikit‑learn)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

# Install Python deps into a virtual environment
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# =========================
# 2️⃣ Runtime stage – minimal image for ECS
# =========================
FROM python:3.10-slim

# Create a non‑root user
RUN useradd --create-home appuser
WORKDIR /app

# Copy only the installed packages from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application source code
COPY . .

# Use the virtual‑env's Python
ENV PATH="/opt/venv/bin:$PATH"

# Expose the port your app listens on
EXPOSE 5000

# Optional health‑check (adjust endpoint if needed)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Run as non‑root
USER appuser

# Start the service with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "application:app"]
