# Homekey Backend

A Flask-based backend application with PostgreSQL database.

## Project Structure
```
homekey-backend/
├── app/
│   ├── __init__.py
│   └── routes.py
├── config.py
├── run.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Running the Application

1. Build and start the containers:
```bash
docker compose up --build -d
docker compose up
```

2. The application will be available at:
- API: http://localhost:5001
- PostgreSQL: http://localhost:5432

### Development

To stop the application:
```bash
docker compose down
```

To view logs:
```bash
docker compose logs
```

To interact with postgresql:
```bash
docker exec -it <postgres_container_id> psql -U postgres homekey
```
