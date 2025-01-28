# Robyn Web API

A modern web API built with [Robyn](https://robyn.tech/) (Python web framework written in **Rust**) featuring user management with [CockroachDB](https://github.com/cockroachdb/cockroach) database integration.

## Features

- ✅ JWT Authentication (Add your implementation details)
- ✅ User CRUD operations
- ✅ [Pydantic](https://docs.pydantic.dev) request/response validation
- ✅ [SQLAlchemy](https://www.sqlalchemy.org/) ORM with Alembic migrations
- ✅ CockroachDB database support
- ✅ Environment configuration with `.env`
- ✅ Hot reload during development

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

2. **Set up virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
# .venv\Scripts\activate   # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Environment Setup**

```bash
cp .env.example .env
# Update .env with your database credentials
```

## Usage

- Development Server

```bash
python -m robyn src/main.py --dev
```

- `--dev` enables hot reload on file changes

- Server runs at `http://localhost:8080`

* Example Requests

```bash
# Create user
curl -X POST http://localhost:8080/user \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "secret"}'

# Get user
curl http://localhost:8080/user/<user-uuid>
```
- Deployment:
```bash
python src/main.py --processes=n --workers=m
```
## Using with Docker

If you want to use this application with Docker, please ensure that you copy the `root.cert` file (downloaded from CockroachDB Cloud) into this directory. This certificate is required to establish a secure connection to the CockroachDB database.

```shell
docker compose up -d --build
```


## Database Migration (Using Alembic)

- Initial Setup

```bash
alembic init alembic
```

Migration Commands:

- `alembic revision --autogenerate -m "message"` - Create new migration
- `alembic upgrade head` - Apply pending migrations
- `alembic downgrade -1` - Rollback last migration
- `alembic current` - Show current revision
- `alembic history` - Show migration history

## Migration Workflow

1. Modify SQLAlchemy models in `src/models.py`

2. Generate migration:

```bash
alembic revision --autogenerate -m "Add new feature"
```

3. Review generated migration file
4. Apply changes:

```bash
alembic upgrade head
```

## Configuration

Required environment variables (`.env file`):

```ini
DATABASE_URL=cockroachdb://user:password@localhost/dbname
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Project Structure

```
.
├── src/
│   ├── main.py        # Main application entry
│   ├── models.py      # SQLAlchemy models
│   ├── schemas.py     # Pydantic models
│   ├── handlers.py    # Business logic
│   ├── routes.py      # API endpoints
│   └── database/      # Database configuration
├── alembic/           # Migration scripts
├── .env.example       # Environment template
├── requirements.txt   # Dependencies
└── README.md          # This file
```

## License

MIT License - see [LICENSE](https://github.com/derder3010/robyn-web-api/blob/main/LICENSE) for details
