# Personal Data Hub

Query your personal data using natural language. Ingest data from GitHub repositories, local documents, exported emails, and markdown notes — then search across all of it with semantic similarity.

## Architecture

```
                    ┌──────────────────────────────┐
                    │     React Frontend (TS)       │
                    │     Vite + Recharts + Tailwind│
                    │     localhost:3000             │
                    └──────────────┬───────────────┘
                                   │ REST
                                   ▼
                    ┌──────────────────────────────┐
                    │     FastAPI Backend (Python)   │
                    │     localhost:8000             │
                    │                                │
                    │  ┌──────────┐ ┌────────────┐  │
                    │  │ Query API│ │ Ingest API │  │
                    │  └────┬─────┘ └─────┬──────┘  │
                    │       │             │          │
                    │  ┌────▼─────────────▼───────┐ │
                    │  │  Embedding Service        │ │
                    │  │  sentence-transformers    │ │
                    │  │  all-mpnet-base-v2 (768d) │ │
                    │  └────┬─────────────────────┘ │
                    └───────┼───────────────────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
     ┌──────────────┐ ┌─────────┐ ┌────────────┐
     │ PostgreSQL   │ │  Redis  │ │ Local Files│
     │ + pgvector   │ │  (RQ)   │ │ (mounted)  │
     │ :5432        │ │  :6379  │ │            │
     └──────────────┘ └─────────┘ └────────────┘
```

### How It Works

1. **Register a data source** — GitHub repo URL, path to documents, mbox file, or notes directory
2. **Trigger ingestion** — ETL pipeline extracts text, chunks it (~512 tokens), generates embeddings via `sentence-transformers`, and stores vectors in pgvector
3. **Search with natural language** — Your query is embedded and compared via cosine similarity against all indexed chunks
4. **View results** — Ranked results with source attribution, similarity scores, and metadata
5. **Dashboard** — Charts showing document distribution, ingestion timeline, and query activity

### Data Flow

```
Source → Ingestor → Text → Chunker → Embeddings → pgvector
                                                      ↑
Query → Embed → Cosine Similarity Search ─────────────┘
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Make (optional, for convenience)

### Run Everything in Docker

```bash
# Clone and start
cp .env.example .env
make docker-up

# Run migrations
docker compose exec backend alembic upgrade head

# Open the app
open http://localhost:3000
```

### Local Development (Recommended)

```bash
# Start infrastructure
docker compose up -d postgres redis

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

## Data Sources

### GitHub Repositories

```json
{
  "name": "My Project",
  "source_type": "github",
  "config": {
    "repo": "owner/repo",
    "include_issues": true,
    "include_prs": true,
    "include_code": true
  }
}
```

Set `GITHUB_TOKEN` in `.env` for higher rate limits (5000 req/hr vs 60).

### Local Documents

```json
{
  "name": "My Docs",
  "source_type": "document",
  "config": {
    "path": "/data/documents",
    "extensions": [".txt", ".pdf", ".md"],
    "recursive": true
  }
}
```

### Exported Emails

```json
{
  "name": "My Emails",
  "source_type": "email",
  "config": {
    "path": "/data/emails.mbox"
  }
}
```

Supports `.mbox` files (e.g., Google Takeout) and directories of `.eml` files. HTML emails are automatically converted to plain text.

### Markdown Notes

```json
{
  "name": "My Notes",
  "source_type": "markdown",
  "config": {
    "path": "/data/notes",
    "recursive": true
  }
}
```

Supports YAML frontmatter. Title and tags are extracted into metadata for filtering.

## API Reference

Base URL: `http://localhost:8000/api/v1`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sources` | GET | List all data sources |
| `/sources` | POST | Register new source |
| `/sources/{id}` | GET/PUT/DELETE | CRUD operations |
| `/sources/{id}/sync` | POST | Trigger ingestion job |
| `/jobs` | GET | List ingestion jobs |
| `/jobs/{id}` | GET/DELETE | Get detail / cancel |
| `/query/search` | POST | Semantic search |
| `/documents` | GET | List/filter documents |
| `/documents/{id}` | GET/DELETE | Get/remove document |
| `/charts/source-distribution` | GET | Docs by source type |
| `/charts/ingestion-timeline` | GET | Ingestion over time |
| `/charts/query-activity` | GET | Query frequency |
| `/health` | GET | Service health check |

### Search Example

```bash
curl -X POST http://localhost:8000/api/v1/query/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "authentication bugs fixed recently",
    "filters": {"source_types": ["github"]},
    "limit": 10
  }'
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.11, FastAPI |
| Frontend | React 18, TypeScript, Vite |
| Vector DB | PostgreSQL 16 + pgvector |
| Embeddings | sentence-transformers (all-mpnet-base-v2, 768d) |
| Task Queue | Redis + RQ |
| Charts | Recharts |
| Styling | Tailwind CSS |
| Infrastructure | Docker Compose |
| CI/CD | GitHub Actions |

## Key Design Decisions

- **HNSW over IVFFlat** — Works correctly regardless of dataset size; IVFFlat requires tuning list count to data volume
- **RQ over Celery** — Simpler for single-machine deployments
- **Content dedup via SHA-256** — Incremental syncs skip unchanged documents
- **Embedding model loaded once** — ~500MB RAM, cached as singleton at startup
- **TanStack Query** — Handles server state, no Redux needed

## Project Structure

```
personal-data-hub/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI route handlers
│   │   ├── models/       # SQLAlchemy ORM models
│   │   ├── schemas/      # Pydantic request/response models
│   │   ├── services/     # Business logic (embedding, search, chunking)
│   │   ├── ingestion/    # ETL pipeline (GitHub, email, docs, markdown)
│   │   └── worker/       # Redis RQ task queue
│   ├── alembic/          # Database migrations
│   └── tests/
├── frontend/
│   └── src/
│       ├── api/          # API client and types
│       ├── components/   # React components
│       ├── pages/        # Page components
│       └── hooks/        # Custom React hooks
├── docker/
├── docker-compose.yml
└── Makefile
```

## Makefile Commands

```bash
make help           # Show all commands
make docker-up      # Start all services
make docker-down    # Stop all services
make dev            # Local dev (infra in Docker)
make migrate        # Run database migrations
make test           # Run all tests
make lint           # Lint everything
make clean          # Remove build artifacts
```

## Environment Variables

See [.env.example](.env.example) for all available configuration options.

## License

MIT
