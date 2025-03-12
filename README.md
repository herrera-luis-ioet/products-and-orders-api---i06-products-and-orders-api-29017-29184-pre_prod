# Products and Orders API with React Frontend

This project consists of a FastAPI backend service for managing products and orders, along with a React frontend for user interaction and a monitoring stack using Prometheus and Grafana.

## Architecture

The application is composed of several services:

- **Frontend**: React application served by Nginx (Port 3001)
- **Backend API**: FastAPI application (Port 8000)
- **Monitoring**:
  - Prometheus (Port 9090)
  - Grafana (Port 3000)

## Prerequisites

- Docker
- Docker Compose
- Git

## Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd products-and-orders-api
   ```

2. Start the services:
   ```bash
   docker-compose up --build
   ```

3. Access the services:
   - Frontend: http://localhost:3001
   - API Documentation: http://localhost:8000/docs
   - Grafana: http://localhost:3000 (admin/admin)
   - Prometheus: http://localhost:9090

## Development Setup

### Backend (FastAPI)

The backend service is built with FastAPI and uses SQLite for data storage.

Environment variables:
- `ENV`: development/production
- `DEBUG`: true/false
- `DATABASE_URL`: SQLite connection string
- `SECRET_KEY`: Secret key for security
- `BACKEND_CORS_ORIGINS`: List of allowed origins

### Frontend (React)

The frontend is built with React and uses Vite as the build tool.

Environment variables:
- `NODE_ENV`: development/production
- `VITE_API_URL`: Backend API URL

### Monitoring

The monitoring stack includes:

- **Prometheus**: Metrics collection and storage
- **Grafana**: Metrics visualization and alerting

Default Grafana credentials:
- Username: admin
- Password: admin

## API Endpoints

### Products

- `GET /api/v1/products`: List all products
- `GET /api/v1/products/{id}`: Get product details
- `POST /api/v1/products`: Create a new product
- `PUT /api/v1/products/{id}`: Update a product
- `DELETE /api/v1/products/{id}`: Delete a product

### Orders

- `GET /api/v1/orders`: List all orders
- `GET /api/v1/orders/{id}`: Get order details
- `POST /api/v1/orders`: Create a new order
- `PUT /api/v1/orders/{id}`: Update an order
- `DELETE /api/v1/orders/{id}`: Delete an order

## Directory Structure

```
.
├── app/                    # Backend application
│   ├── api/               # API endpoints
│   ├── crud/              # Database operations
│   ├── models/            # Database models
│   └── schemas/           # Pydantic schemas
├── frontend/              # Frontend application
│   ├── src/              # Source code
│   └── nginx.conf        # Nginx configuration
├── monitoring/           # Monitoring configuration
│   ├── grafana/         # Grafana configuration
│   └── prometheus/      # Prometheus configuration
├── tests/               # Test suite
├── docker-compose.yml   # Docker services configuration
└── README.md           # This file
```

## Testing

Run the test suite:

```bash
# Backend tests
docker-compose exec api pytest

# Frontend tests
docker-compose exec frontend npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]