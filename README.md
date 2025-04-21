# 📦 ParcelLab Backend Challenge

A robust FastAPI + PostgreSQL backend service for tracking shipments and enriching delivery locations with weather data. Built with a focus on clean architecture, caching, retry mechanisms, and developer experience.

---

## ✨ Features

- 🔍 **Track shipments** by tracking number and carrier
- 🔗 **Filter and paginate** shipments by status and carrier
- 🌦 **Live weather data** fetched from OpenWeatherMap based on ZIP codes
- 🔁 **Retry logic** for unstable external API requests
- ⚡️ **Redis caching** for efficient weather retrieval
- 📚 **Interactive API docs** via Swagger and ReDoc
- 🧪 **Test coverage** with Pytest, CI, and linting
- 🧰 **Developer tools**: Makefile, GitHub Actions, pre-commit

---

## 🧰 Tech Stack

| Layer           | Tech                              |
|----------------|-----------------------------------|
| API            | FastAPI, Pydantic                 |
| Database       | PostgreSQL, SQLAlchemy, Alembic   |
| Caching        | Redis                             |
| Infrastructure | Docker, Docker Compose            |
| Testing        | Pytest, Coverage, GitHub Actions  |
| Tooling        | Pre-commit, Black, Flake8, Mypy   |

---

## 🚀 Getting Started

### 📦 Prerequisites

- [Docker](https://www.docker.com/) & Docker Compose
- Python 3.11+ (for running local tools)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pre-commit install
```

### 📁 Setup

1. **Clone the repository**:
```bash
git clone https://github.com/amalgmar/parcellab-backend-challenge.git
cd parcellab-backend-challenge
```

2. **Set environment variables**:
```bash
cp .env.example .env
```

3. **Start the system**:
```bash
make build
make start
```

4. **(Optional)** DB setup:
```bash
make migrate   # Prompted if schema changes
make seed      # Seeds the DB (already triggered on startup)
```

5. **(Optional)** Run test suite:
```bash
make test
```

---

## 🔍 API Documentation

- Swagger UI: [http://localhost:8080/docs](http://localhost:8080/docs)
- ReDoc: [http://localhost:8080/redoc](http://localhost:8080/redoc)

These are generated automatically from Pydantic models, route metadata, and docstrings using FastAPI’s OpenAPI integration.

> Includes grouped tags (`Shipments`), custom query descriptions, and typed responses.

---

## 📜 Makefile Commands

```bash
make help
```

| Command        | Description                                 |
|----------------|---------------------------------------------|
| `make start`   | 🔹 Start all Docker services                |
| `make stop`    | 🔺 Stop running services                    |
| `make build`   | 🔧 Build backend, DB, and Redis             |
| `make test`    | 🧪 Run tests with coverage report           |
| `make lint`    | 🛃 Run pre-commit: flake8, black, pylint    |
| `make migrate` | 🗃 Prompt to generate Alembic migration     |
| `make seed`    | 🌱 Populate DB with sample data             |
| `make shell`   | 🔍 Open shell inside backend container      |

---

## 📂 Project Structure

```
├── app
│   ├── api/routes         # FastAPI routes
│   ├── models             # SQLAlchemy models
│   ├── schemas            # Pydantic DTOs
│   ├── services           # Business logic
│   ├── utils              # Helpers (e.g. zip extraction)
│   ├── scripts            # Seeder scripts
│   └── tests              # Unit and integration tests
├── alembic                # Database migrations
├── Makefile               # CLI commands
├── docker-compose.yml     # Containers: API, DB, Redis
└── .pre-commit-config.yaml
```

---

## 🚦 CI/CD

- GitHub Actions run on every `push` and `pull_request`
- Linting (Black, Flake8, Pylint), typing (Mypy), and tests (Pytest)
- Coverage reports uploaded to [Codecov](https://about.codecov.io/)

---

## 👨‍💼 Discussion Points

> ✅ Covered by the current design and code

- **Design choices**:
  - Used class-based schemas and declarative routes for maintainability
  - Added retry + cache on weather API to minimize latency
  - Chose sync SQLAlchemy for easier setup; async-ready architecture

- **To deploy to production**:
  - Use `.env` securely (e.g., Docker secrets or CI inject)
  - Add HTTPS reverse proxy (e.g., Nginx, Caddy)
  - Enable logging (e.g., ELK, Datadog)

- **To scale to 1000 RPS**:
  - Switch to async (FastAPI + httpx + asyncpg)
  - Enable horizontal scaling with a load balancer
  - Move Redis & DB to managed services
  - Add rate-limiting, monitoring, and circuit breakers

---

## 🙌 Contributors

**Amal Gmar**
📧 [amalgmar7@gmail.com](mailto:amalgmar7@gmail.com)
🔍 [@amalgmar](https://github.com/amalgmar)

---

## 🧪 Future Improvements

- [ ] ✅ Switch to **Async I/O** with `httpx.AsyncClient` and `asyncpg` for non-blocking performance
- [ ] ♻️ **Weather caching** enhancements with expiration & invalidation strategies
- [ ] 📈 Integrate **Prometheus & Grafana** for monitoring, alerts, and metrics
- [ ] 🔐 Add **rate limiting** and security middleware for public-facing endpoints
- [ ] 🚀 CI/CD deployment to cloud environments (e.g., AWS, Render, Railway)
- [ ] 🔄 Webhook support for carrier updates (event-driven architecture)
