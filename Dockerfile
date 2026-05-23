# =========================
# 1️⃣ Builder stage – install deps
# =========================
FROM python:3.10-slim AS builder

# Create a virtual environment in /opt/venv
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV

# Ensure pip is up‑to‑date
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade pip

# Install application dependencies
# (Assumes you have a requirements.txt at the repository root)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =========================
# 2️⃣ Runtime stage – minimal image for ECS
# =========================
FROM python:3.10-slim

# Create a non‑root user
RUN useradd --create-home appuser
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application source code
COPY . .

# Adjust ownership so the non‑root user can read/write
RUN chown -R appuser:appuser /app

# Activate the virtual‑env's Python
ENV PATH="/opt/venv/bin:$PATH"

# (Optional) Remove the healthcheck if you haven’t set it up yet
# HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
#   CMD curl -f http://localhost:5000/health || exit 1

# Run as the non‑root user
USER appuser

# Start the service with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "application:app"]
