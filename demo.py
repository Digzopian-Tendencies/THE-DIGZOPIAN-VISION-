version: "3.9"

services:
  orchestrator:
    build: ./agents/orchestrator
    ports:
      - "8000:8000"
    env_file: .env
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
