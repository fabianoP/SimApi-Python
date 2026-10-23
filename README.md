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

Development defaults are included so the stack can start without an environment file. For custom values, copy the provided template:

```bash
cp src/.env.example src/.env
```

Then edit `src/.env`:

```dotenv
DJANGO_SECRET_KEY=replace-with-a-random-value
DJANGO_DEBUG=false
POSTGRES_PASSWORD=replace-app-database-password
CELERY_DB_PASSWORD=replace-celery-database-password
RABBITMQ_USER=user
RABBITMQ_PASSWORD=replace-broker-password
RABBITMQ_VHOST=vhost
```

`.env` is ignored by Git. `.env.example` contains placeholders only and is safe to commit. Do not commit real credentials.

The client scripts also accept:

- `SIMAPI_URL` (default: `http://localhost:8000`)
- `SIMAPI_EMAIL`
- `SIMAPI_USER`
- `SIMAPI_PASSWORD`

## Quick start

### 1. Get the modernized branch

```bash
git clone https://github.com/fabianoP/SimApi-Python.git
cd SimApi-Python
git switch modernize-stack
```

If the repository is already cloned:

```bash
git fetch origin
git switch modernize-stack
git pull --ff-only
```

### 2. Start Docker

Start Docker Desktop on macOS/Windows, or Docker Engine on Linux. Confirm that Docker Compose v2 is available:

```bash
docker version
docker compose version
```

On Apple Silicon, ensure Docker Desktop can run `linux/amd64` images. The first generator/simulator build can take several minutes because it downloads and installs the pinned EnergyPlus and scientific Python toolchains.

### 3. Configure the stack (optional)

The development defaults work without a `.env` file. For custom credentials, copy `src/.env.example` to `src/.env` as shown in [Configuration](#configuration). Use the same values consistently; Compose passes them to RabbitMQ, PostgreSQL, Django, and Celery.

### 4. Build and start the services

From the repository root:

```bash
cd src
docker compose up --build -d
```

Check startup status:

```bash
docker compose ps
docker compose logs -f web web_worker generator simulator
```

Wait until `db`, `rabbitmq`, `web`, and `generator` are healthy and the simulator services are running. Press `Ctrl-C` to stop following logs; the containers continue running in the background.

The exposed services are:

- API and GraphQL: <http://localhost:8000/>
- RabbitMQ management: <http://localhost:15672/>
- Generator API: <http://localhost:8001/>
- First simulator API: <http://localhost:8002/>

A quick API readiness check is:

```bash
curl --fail http://localhost:8000/user/
```

### 5. Install the client dependency

Open a second terminal in the repository root (not `src`) and create a virtual environment:

```bash
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip requests
```

Windows PowerShell activation:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip requests
```

### 6. Initialize the example model

The client defaults to a local development user. You can use those defaults directly:

```bash
python initialize_model.py example-model
```

This uploads `test_setup_files/update.idf` and `test_setup_files/update.epw`, creates the API user if necessary, and starts FMU generation. Follow its progress with:

```bash
cd src
docker compose logs -f web_worker generator simulator
```

Wait for the simulator log to show that the FMU/model has initialized before sending time-step inputs. On Apple Silicon, this stage can be noticeably slower because the generator and simulator run under x86_64 emulation.

To use different local client credentials, set the same values in both client terminals:

```bash
export SIMAPI_EMAIL="user@user.com"
export SIMAPI_USER="user"
export SIMAPI_PASSWORD="user user88"
```

PowerShell equivalents:

```powershell
$env:SIMAPI_EMAIL = "user@user.com"
$env:SIMAPI_USER = "user"
$env:SIMAPI_PASSWORD = "user user88"
```

Custom model files and simulation parameters are supported:

```bash
python initialize_model.py example-model \
  --idf path/to/model.idf \
  --epw path/to/weather.epw \
  --step-size 600 \
  --final-time 24
```

`--final-time` is measured in hours. The IDF must be compatible with the bundled EnergyPlus 9.0.1 IDD.

### 7. Run the initialized model

From the repository root with the virtual environment active:

```bash
python run_initialized_model.py example-model
```

The default run sends a time step every 600 seconds over a simulated 24-hour duration. The runner waits up to five minutes for each output and prints each returned result.

Override the run parameters when needed:

```bash
python run_initialized_model.py example-model \
  --duration 86400 \
  --step-size 600 \
  --shade 1.0 \
  --poll-interval 0.5 \
  --poll-timeout 300
```

`--duration` and `--step-size` are measured in seconds. Use the same step size passed to `initialize_model.py`.

### 8. Scale simulators (optional)

From `src`, start several simulator replicas:

```bash
docker compose up -d --scale simulator=5
```

Inspect the replicas and their logs with:

```bash
docker compose ps simulator
docker compose logs -f simulator
```

### 9. Stop or reset the stack

Stop and remove containers while preserving PostgreSQL and RabbitMQ data:

```bash
cd src
docker compose down
```

Remove containers and all application/broker data for a clean restart:

```bash
docker compose down --volumes
```

After a full reset, rerun `docker compose up --build -d` and initialize the model again.

## Troubleshooting

### A service does not become healthy

```bash
cd src
docker compose ps
docker compose logs --tail=200 db rabbitmq web web_worker generator simulator
```

Resolve the first unhealthy dependency before restarting with `docker compose up -d`.

### Port already in use

The stack binds ports `8000`, `8001`, `8002-8102`, `5433`, `5434`, `5672`, and `15672`. Stop the conflicting process or change the corresponding host-side port in `src/docker-compose.yml`.

### FMU generation or simulation fails

Confirm that the IDF is compatible with EnergyPlus 9.0.1 and inspect generator/simulator logs:

```bash
cd src
docker compose logs --tail=300 generator simulator
```

### Client authentication fails

Use the same `SIMAPI_EMAIL` and `SIMAPI_PASSWORD` values for initialization and execution. To recreate the development user and all data, run `docker compose down --volumes`, restart the stack, and initialize again.

### Clean rebuild

```bash
cd src
docker compose down --volumes
docker compose build --no-cache
docker compose up -d
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
