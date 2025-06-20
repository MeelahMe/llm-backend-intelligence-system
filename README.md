# LLM Backend Intelligence System

LLM Backend Intelligence System is a production-ready backend service that transforms raw alerts from observability platforms into human-readable incident summaries using large language models (LLMs). This project helps DevOps and SRE teams reduce alert fatigue, accelerate incident triage, and improve operational awareness across complex systems.

> Ingest alerts → Enrich context using LLMs → Push human-readable summaries via API or Slack

---

## Features

- **FastAPI backend** for structured alert ingestion and retrieval
- **LLM-powered summarization** using OpenAI or Gemini
- **Asynchronous task queue** for background processing
- **Slack and webhook integration** for real-time alert delivery
- **Token usage and latency tracking** for every LLM call
- **PostgreSQL storage** for audit history and traceability
- **Dockerized environment** with CI/CD integration
- **Ready for extensibility** via modular service layers

---

## Use Case

Send raw alert data from a monitoring system (e.g., Prometheus):

```json
{
  "source": "prometheus",
  "alert": "InstanceDown",
  "labels": {
    "instance": "web-03",
    "severity": "critical"
  },
  "annotations": {
    "description": "web-03 has been down for 5 minutes"
  }
}
```

Receive a summarized, LLM-generated explanation:

{
  "summary": "⚠️ Instance 'web-03' has been unresponsive for 5 minutes. This usually indicates a crash or network issue. Suggested action: SSH into the instance and check logs for nginx and systemd."
}

## Architecture Overview

    - FastAPI handles RESTful alert ingestion and summary retrieval
    - Celery + Redis manage alert processing and retries
    - OpenAI or Gemini performs natural language summarization
    - PostgreSQL stores alerts, summaries, and metrics
    - SlackNotifier pushes summaries to relevant teams

See `system_design.md` for architectural details.

## Get Started

### Prerequisites

- Python 3.10+
- Docker + Docker Compose
- Redis (for queue)
- PostgreSQL (or use Docker for everything)

### Install 

```bash
# Clone the repo
git clone https://github.com/MeelahMe/llm-backend-intelligence-system.git
cd llm-backend-intelligence-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start app (without queue)
uvicorn app.main:app --reload
```

## Run with Docker 

The project includes a preconfigured docker-compose.yml file to simplify setup. This runs:

- The FastAPI app
- A Redis queue (for background task processing)
- PostgreSQL (for storing alerts and summaries)
(- Optional) A Celery worker container

1. Build and start all services 

```bash
docker-compose up --build
```

This will:

- Build the FastAPI app image
- Pull and run Redis and PostgreSQL
- Start all services on the correct ports

2. Open in browser

once running, visit :

- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health