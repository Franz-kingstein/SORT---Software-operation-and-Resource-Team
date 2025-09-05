# SORT Backend + Frontend Dockerfile
FROM python:3.12-slim AS backend

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y git build-essential && rm -rf /var/lib/apt/lists/*

# Copy backend code
COPY ./src ./src
COPY ./sort_env ./sort_env
COPY ./requirements.txt ./requirements.txt
COPY .env .env

# Install Python deps
RUN python -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install fastapi uvicorn httpx python-dotenv starlette pydantic openai PyGithub crewai langchain

# Expose backend port
EXPOSE 8000

# --- Frontend ---
FROM node:20-slim AS frontend
WORKDIR /frontend
COPY ./frontend ./frontend
RUN cd frontend && npm install && npm run build

# --- Final image ---
FROM python:3.12-slim
WORKDIR /app

# Copy backend from backend stage
COPY --from=backend /app /app
# Copy frontend build from frontend stage
COPY --from=frontend /frontend/frontend/dist /app/frontend_dist

ENV PYTHONPATH=/app/src
ENV PORT=8000

# Entrypoint: run backend (FastAPI) and serve frontend static files
CMD ["/app/venv/bin/uvicorn", "sort.backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
