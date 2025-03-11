# Product and Order Management Component

A comprehensive API for managing products and orders using FastAPI, SQLAlchemy, and SQLite.

## Project Overview

This component provides a RESTful API for managing products and orders in an e-commerce system. It allows for:

- Product management (CRUD operations)
- Order processing and management
- Inventory tracking
- Basic reporting and analytics

### Core Technologies

- **Backend**: Python 3.9+, FastAPI v0.115
- **Database**: SQLite 3 with SQLAlchemy ORM
- **Validation**: Pydantic
- **Documentation**: Swagger/OpenAPI
- **Testing**: pytest

## Installation

### Prerequisites

- Python 3.9 or higher
- Poetry (Python package manager)

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd products-and-orders-api
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```bash
   alembic upgrade head
   ```

## Usage

### Starting the API Server

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## Development

### Project Structure

```
app/
├── api/              # API routes
├── core/             # Core functionality, config
├── crud/             # CRUD operations
├── db/               # Database models and session
├── models/           # SQLAlchemy models
├── schemas/          # Pydantic schemas
└── services/         # Business logic
tests/                # Test suite
alembic/              # Database migrations
```

### Code Style

This project uses:
- Black for code formatting
- Flake8 for linting
- isort for import sorting
- mypy for type checking

Run the formatters:
```bash
black .
isort .
```

Run the linters:
```bash
flake8
mypy .
```

### Pre-commit Hooks

Install pre-commit hooks:
```bash
pre-commit install
```

## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app
```

## Deployment

### Docker

Build the Docker image:
```bash
docker build -t products-and-orders-api .
```

Run the container:
```bash
docker run -p 8000:8000 products-and-orders-api
```

### Docker Compose

For local development with monitoring tools:

```bash
docker-compose up -d
```

This will start:
- The API service with hot-reload enabled
- Prometheus for metrics collection
- Grafana for metrics visualization (available at http://localhost:3000)

### CI/CD Pipeline

This project uses GitHub Actions for continuous integration and delivery:

- **Linting**: Runs Black, isort, Flake8, and MyPy
- **Testing**: Runs pytest with coverage reporting
- **Building**: Builds and pushes Docker image on successful merge to main branch or when tags are pushed

The workflow is defined in `.github/workflows/ci.yml`.

## License

[Specify your license here]

## Contributing

[Contribution guidelines]
