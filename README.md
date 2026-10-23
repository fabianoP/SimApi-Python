# SimApi Building Energy Co-Simulation Platform

SimApi coordinates EnergyPlus Functional Mock-up Units (FMUs) through a Django REST/GraphQL API, Celery workers, RabbitMQ, PostgreSQL, and scalable simulator containers.

## Architecture

- `web`: Django 5 REST and GraphQL API
- `web_worker`: Celery worker for API-to-simulator tasks
- `generator`: converts EnergyPlus IDF/EPW inputs into FMUs
- `simulator`: runs FMUs with PyFMI and Assimulo
- `rabbitmq`: Celery broker
- `db`: application database
- `celery_result_db`: Celery result database

## Prerequisites

- Docker Engine or Docker Desktop with Docker Compose v2
- At least 8 GB of memory for a single simulator
- Python 3.12 if running API checks or the client scripts directly

### Apple Silicon

EnergyPlus 9.0.1 and the required FMU toolchain are distributed for x86_64 Linux. The generator and simulator therefore run as `linux/amd64` containers. Docker Desktop can run them through emulation on Apple Silicon, but builds and simulations will be slower than on an x86_64 host.

## Configuration

Development defaults are included so the stack can start without an environment file. Override them in your shell or a local `.env` file before non-local use:

```dotenv
DJANGO_SECRET_KEY=replace-with-a-random-value
DJANGO_DEBUG=false
POSTGRES_PASSWORD=replace-app-database-password
CELERY_DB_PASSWORD=replace-celery-database-password
RABBITMQ_USER=user
RABBITMQ_PASSWORD=replace-broker-password
RABBITMQ_VHOST=vhost
```

`.env` is ignored by Git. Do not commit credentials.

The client scripts also accept:

- `SIMAPI_URL` (default: `http://localhost:8000`)
- `SIMAPI_EMAIL`
- `SIMAPI_USER`
- `SIMAPI_PASSWORD`

## Build and run

From the repository root:

```bash
cd src
docker compose build
docker compose up
```

Compose waits for PostgreSQL, RabbitMQ, the API, and the generator health checks before starting dependent services. The API is available at <http://localhost:8000/> and RabbitMQ management at <http://localhost:15672/>.

Run multiple simulators with:

```bash
docker compose up --scale simulator=5
```

Stop the stack with `Ctrl-C`, then remove containers while retaining data:

```bash
docker compose down
```

Remove containers and database/broker volumes:

```bash
docker compose down --volumes
```

## Initialize and run a model

Install the client dependency in a virtual environment:

```bash
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install requests
```

Initialize a model using the included example files:

```bash
python initialize_model.py example-model
```

Custom files and simulation parameters are supported:

```bash
python initialize_model.py example-model \
  --idf path/to/model.idf \
  --epw path/to/weather.epw \
  --step-size 600 \
  --final-time 24
```

After the generator and simulator report that the model is ready, run it:

```bash
python run_initialized_model.py example-model
```

The runner has bounded polling and configurable duration:

```bash
python run_initialized_model.py example-model \
  --duration 86400 \
  --step-size 600 \
  --shade 1.0 \
  --poll-timeout 300
```

## Local API development

Create a Python 3.12 virtual environment and install the web requirements:

```bash
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r src/simapi_web/requirements.txt
```

Run checks and tests without PostgreSQL or RabbitMQ:

```bash
cd src/simapi_web
python manage.py check --settings=simapi_web.test_settings
python manage.py makemigrations --check --dry-run --settings=simapi_web.test_settings
python manage.py test --settings=simapi_web.test_settings
```

The full FMU simulator remains container-oriented because PyFMI, Assimulo, and EnergyPlus require a pinned native toolchain.

## Project layout

```text
.
├── initialize_model.py
├── run_initialized_model.py
├── src
│   ├── docker-compose.yml
│   ├── simapi_web
│   └── simapi_simulation
│       ├── fmu_generator
│       └── fmu_simulator
└── test_setup_files
```

## Continuous integration

GitHub Actions compiles all Python sources, validates Django configuration and migration state, runs the API tests, and validates the primary Compose configuration.
