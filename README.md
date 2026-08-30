# LLM Backend Intelligence System

LLM Backend Intelligence System is a backend service that transforms raw alerts from observability platforms into human-readable incident summaries using an LLM. It's built for DevOps and SRE teams who want to reduce alert fatigue and speed up triage by turning raw alert payloads into a plain-English explanation.

Ingest alert → Summarize with an LLM (mock or OpenAI) → Return the summary

## Current status

This is a working prototype, not a production deployment. The core alert-summarization flow is implemented and tested; the surrounding infrastructure described in [`system_design.md`](system_design.md) (async queue, persistence, Slack delivery) is the target architecture and is not yet built. See [Roadmap](#roadmap) below for what's planned vs. what's real today.

## Features

**Implemented:**
- FastAPI backend with a single alert-ingestion endpoint
- LLM-powered summarization via OpenAI, with a mock LLM client for local development and testing (no API key or cost required)
- API key authentication and rate limiting (10 req/min) on `POST /alerts/`
- Pydantic-validated request/response schemas, including a typed `AlertResponse`
- CI pipeline: tests, gitleaks, Semgrep, Bandit, and a Trivy container scan on every push, all GitHub Actions pinned to commit SHA
- Test suite covering the happy path, validation errors, auth (missing/wrong/valid key), the LLM-failure error path, and a real-OpenAI integration test (skipped automatically without a live key) - 85% coverage
- **Documented prompt injection finding and fix** for the alert-summarization endpoint - see [Security](#security) below

**Not yet implemented** (described in the architecture doc as planned, not current):
- Asynchronous processing via Redis/Celery
- PostgreSQL persistence — summaries are not currently stored or retrievable after the request completes
- Slack/webhook delivery
- Gemini support (OpenAI only, for now)

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

```json
{
  "summary": "Instance 'web-03' has been unresponsive for 5 minutes. This usually indicates a crash or network issue. Suggested action: SSH into the instance and check logs for nginx and systemd."
}
```

With the mock LLM client, the response also includes simulated token usage and cost fields (`token_usage`, `cost_usd`). These are not currently populated on real OpenAI calls.

## Architecture Overview

The current implementation is a synchronous request/response flow:

- FastAPI receives and validates the alert via `POST /alerts/`
- A pluggable `LLMClient` interface (mock or OpenAI, selected via environment variables) generates the summary
- The summary is returned directly in the response — nothing is persisted or queued

The originally planned architecture — an async queue (Redis/Celery), PostgreSQL storage, and a Slack/webhook notifier — is documented in [`system_design.md`](system_design.md) as the target design. That layer does not exist in the code yet.

## Security

`annotations.description` is fully attacker-controllable free text that reaches the LLM prompt. A real prompt injection vulnerability was found here, tested live against `gpt-3.5-turbo`, and fixed iteratively (the first mitigation attempt only partially closed the most dangerous attack vector; a second revision closed it, confirmed with repeated test runs).

Full methodology, results, and honestly-scoped limitations: [`docs/security-findings.md`](docs/security-findings.md).

## Get Started

### Prerequisites

- Python 3.10+
- An OpenAI API key (optional — the mock LLM client works without one)

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
```

### Configure

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

```env
LLM_PROVIDER=openai
USE_MOCK_LLM=true       # set to false to use a real OpenAI call
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.3
OPENAI_TIMEOUT=10
```

Leave `USE_MOCK_LLM=true` to run and test the service with no API key and no cost.

### Run

```bash
uvicorn app.main:app --reload
```

Then visit:
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

> **Note:** The `Dockerfile` builds and runs correctly (`docker build -t llm-backend .`). `docker-compose.yml` is currently empty — a full Compose setup (with Redis/Postgres once those exist) is still planned.

## API Reference

- `GET /health` — health check
- `POST /alerts/` — ingest an alert and receive an LLM-generated summary. Requires an `X-API-Key` header matching the server's configured `API_KEY`; unauthenticated or incorrect requests receive a 401. Rate-limited to 10 requests/minute per IP.

## Project Structure

```bash
llm-backend-intelligence-system/
├── app/
│   ├── config/          # Settings (env-driven)
│   ├── routes/           # API endpoints (alerts)
│   ├── schemas/          # Pydantic request/response schemas
│   ├── services/         # LLM client interface + mock/OpenAI implementations
│   ├── auth.py           # API key verification dependency
│   ├── rate_limit.py      # slowapi rate limiter
│   └── main.py             # FastAPI app instance
├── tests/                # Unit tests (auth, error handling, alerts, health)
├── scripts/              # Manual scripts (e.g. prompt injection PoC - not part of CI)
├── docs/
│   └── security-findings.md   # Prompt injection finding, fix, and results
├── .github/workflows/security.yml   # CI: tests + gitleaks + Semgrep + Bandit + Trivy
├── system_design.md      # Target architecture (see Current status above)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml     # Currently empty — see note above
└── README.md
```
## Testing

This project uses `pytest`. Tests cover the health endpoint, alert creation (mock LLM), request validation, and a real-OpenAI integration test that's skipped automatically unless a valid `OPENAI_API_KEY` is set and `USE_MOCK_LLM=false`.

```bash
pytest tests/
```

With coverage:

```bash
pip install pytest-cov
pytest --cov=app tests/
```

## Roadmap

Planned work to close the gap between this README and `system_design.md`:

- [x] CI pipeline (tests, dependency/secret/SAST scanning)
- [x] Basic auth / rate limiting on `POST /alerts/`
- [x] Adversarial testing of the summarization endpoint (prompt injection via `annotations.description`) with documented findings and mitigations - see [Security](#security)
- [ ] Automated adversarial scanning (e.g. Garak or PyRIT) added as a CI step, to catch prompt regressions automatically
- [ ] Extend injection testing to the `source` and `alert` fields
- [ ] Async processing via Redis + Celery
- [ ] PostgreSQL persistence and a real `GET /alerts/{id}/summary` endpoint
- [ ] Slack/webhook delivery
- [ ] Gemini support alongside OpenAI
