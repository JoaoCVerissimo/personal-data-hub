.PHONY: help dev dev-backend dev-frontend docker-up docker-down migrate migrate-create test test-backend test-frontend lint lint-backend lint-frontend clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

docker-up: ## Start all services via Docker Compose
	docker compose up --build -d

docker-down: ## Stop all services
	docker compose down

docker-logs: ## Tail logs for all services
	docker compose logs -f

dev: ## Start infra in Docker, backend + frontend locally
	docker compose up -d postgres redis
	@echo "Waiting for services to be healthy..."
	@sleep 3
	$(MAKE) dev-backend &
	$(MAKE) dev-frontend

dev-backend: ## Start backend in dev mode
	cd backend && uvicorn app.main:app --reload --port 8000

dev-frontend: ## Start frontend in dev mode
	cd frontend && npm run dev

migrate: ## Run Alembic migrations
	cd backend && alembic upgrade head

migrate-create: ## Create new migration (usage: make migrate-create MSG="add xyz")
	cd backend && alembic revision --autogenerate -m "$(MSG)"

test: test-backend test-frontend ## Run all tests

test-backend: ## Run backend tests
	cd backend && pytest tests/ -v

test-frontend: ## Run frontend tests
	cd frontend && npm test -- --run

lint: lint-backend lint-frontend ## Lint everything

lint-backend: ## Lint backend
	cd backend && ruff check . && mypy app/ --ignore-missing-imports

lint-frontend: ## Lint frontend
	cd frontend && npm run lint && npm run typecheck

clean: ## Remove build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf backend/.venv frontend/node_modules frontend/dist
