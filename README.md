# TRON Scanner API

A microservice built with FastAPI for scanning and retrieving information about TRON blockchain addresses.

## Features

- Get TRON wallet information (balance, bandwidth, energy)
- Store wallet information in a database
- Paginated retrieval of all stored addresses
- Docker-based deployment

## Tech Stack

- **Backend**: FastAPI, Python 3.11
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy (Async)
- **Migrations**: Alembic
- **TRON Integration**: tronpy
- **Containerization**: Docker, Docker Compose

## Prerequisites

- Docker and Docker Compose
- Git

## Installation and Setup

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd trpn_ms
   ```

2. Create a `.env` file (or use the existing one) with the following variables:
   ```
   DB_HOST=postgres
   DB_PORT=5432
   DB_NAME=tron_db
   DB_USER=admin
   DB_PASSWORD=root
   ```

3. Start the application with Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. The API will be available at http://localhost:8000

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd trpn_ms
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   # On Windows
   .\env\Scripts\activate
   # On macOS/Linux
   source env/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # for development tools
   ```

4. Set up a PostgreSQL database and update the `.env` file with appropriate connection details.

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the application:
   ```bash
   python -m app.main
   ```

7. The API will be available at http://localhost:8000

## API Endpoints

- `POST /api/tron/get-address-info` - Get information about a TRON address
  - Request body: `{ "address": "TRX_ADDRESS" }`

- `GET /api/tron/get-all-addresses` - Get all stored addresses (paginated)
  - Query parameters: `page` and `size` for pagination

## Testing

Run tests with pytest:
```bash
pip install -r requirements-test.txt
pytest
```

## Health Check

The service includes a health check endpoint at the root URL (`/`), which returns basic service information.

## License

MIT License