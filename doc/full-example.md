# Full End-to-End Co-Simulation Example

This guide walks through a complete co-simulation session with SimApi using the bundled EnergyPlus 9.0.1 building model (`test_setup_files/update.idf`) and weather file (`test_setup_files/update.epw`).

---

## 1. Start the Container Stack

From the repository root, build and start all seven services:

```bash
cd src
docker compose up --build -d
```

Verify that all containers are running and healthy:

```bash
docker compose ps
```

Expected status output:

```text
NAME                        SERVICE            STATUS                   PORTS
simapi-celery_result_db-1   celery_result_db   Up (healthy)             0.0.0.0:5434->5432/tcp
simapi-db-1                 db                 Up (healthy)             0.0.0.0:5433->5432/tcp
simapi-generator-1          generator          Up (healthy)             0.0.0.0:8001->8000/tcp
simapi-rabbitmq-1           rabbitmq           Up (healthy)             0.0.0.0:5672->5672/tcp, 0.0.0.0:15672->15672/tcp
simapi-simulator-1          simulator          Up                       0.0.0.0:8002->8000/tcp
simapi-web-1                web                Up (healthy)             0.0.0.0:8000->8000/tcp
simapi-web_worker-1         web_worker         Up
```

Check API readiness from the host:

```bash
curl --fail http://localhost:8000/user/
```

Expected response:

```json
[]
```

> **Note (Port `8000` conflict):** If another process on your machine is already bound to `localhost:8000`, either stop that process, set `SIMAPI_URL` to an alternate host/port, or run the client scripts directly inside the `web` container (`docker compose exec web ...`).

---

## 2. Set Up the Client Environment

In a second terminal at the repository root (outside `src/`), create a Python 3.12 virtual environment and install `requests`:

```bash
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip requests
```

---

## 3. Initialize the EnergyPlus FMU Model

Run [`initialize_model.py`](../initialize_model.py) to create/authenticate the default user, upload `test_setup_files/update.idf` and `test_setup_files/update.epw`, and trigger FMU compilation and initialization:

```bash
python initialize_model.py example-model \
  --idf test_setup_files/update.idf \
  --epw test_setup_files/update.epw \
  --step-size 600 \
  --final-time 24
```

Expected response from `POST /init_model/`:

```json
{
  "model_name": "example-model",
  "user": 1,
  "container_id": "simulator",
  "idf_file": "http://localhost:8000/Media/update.idf",
  "epw_file": "http://localhost:8000/Media/update.epw",
  "step_size": 600,
  "final_time": "24.0",
  "created_on": "2026-10-23T21:09:36.988160Z"
}
```

### Watch FMU Generation and Simulator Initialization

Follow the worker, generator, and simulator logs until the EnergyPlus FMU slave is initialized:

```bash
cd src
docker compose logs -f web_worker generator simulator
```

You will see the three-stage pipeline complete:

1. **`web_worker` forwards the uploaded `.idf` and `.epw` to `simulator`**:
   ```text
   web_worker-1 | Posting model example-model to http://simulator:8000/upload/example-model
   web_worker-1 | Task rest_api.tasks.post_model[...] succeeded in 0.14s: 200
   ```
2. **`generator` compiles `example_model.fmu` via `EnergyPlusToFMU`**:
   ```text
   generator-1  | ! EnergyPlusToFMU.py -- Begin exporting IDF file {.../example-model.idf} as an FMU
   generator-1  | ! EnergyPlusToFMU.py -- Using model identifier {example_model}
   generator-1  | ! makeFMULib.py -- FMU shared library {example_model.so} has address size {64}
   generator-1  | ! EnergyPlusToFMU.py -- Creating zip file {example_model.zip}, with compression on
   generator-1  | ! EnergyPlusToFMU.py -- Renaming completed zip file {example_model.zip} to {example_model.fmu}
   generator-1  | Task generator_tasks.gen_fmu[...] succeeded in 21.35s: 'success'
   ```
3. **`simulator` loads the FMU with PyFMI and initializes EnergyPlus 9.0.1**:
   ```text
   simulator-1  | Task simulator_tasks.set_model[...] succeeded in 5.16s: None
   simulator-1  | FMU location handler COMPLETE
   simulator-1  | EnergyPlus Starting
   simulator-1  | EnergyPlus, Version 9.0.1-bb7ca4f0da
   simulator-1  | Instantiating FunctionalMockupUnitExport interface
   simulator-1  | ExternalInterface initializes.
   simulator-1  | [INFO][Slave] [ok][FMU status:OK] fmiInitializeSlave: The connection has been accepted.
   simulator-1  | [INFO][Slave] [ok][FMU status:OK] fmiInitializeSlave: Slave Slave is initialized.
   simulator-1  | Number of outputs in ExternalInterface = 3
   simulator-1  | Number of inputs  in ExternalInterface = 1
   simulator-1  | Starting Simulation at 01/01/2011 for RUNPERIOD 1
   simulator-1  | ExternalInterface starts first data exchange.
   ```

Once `ExternalInterface starts first data exchange.` appears in the `simulator` logs, the model is ready to step through time.

---

## 4. Run the Co-Simulation Time Steps

From the repository root, execute [`run_initialized_model.py`](../run_initialized_model.py). Below is a 1-hour (`3600` seconds) run with 10-minute (`600` seconds) time steps and a shading control signal of `yShadeFMU = 1.0`:

```bash
python run_initialized_model.py example-model \
  --duration 3600 \
  --step-size 600 \
  --shade 1.0 \
  --poll-interval 0.5 \
  --poll-timeout 300
```

Expected console output:

```text
Running 1 model(s): ['example-model']
Sim: example-model | Time: 0 | Output: [{'outputJson': '{"TRoo": 14.99999999999973, "dryBulb": -6.333333333333334, "ZoneSens": 1244.017637607269}'}]
Sim: example-model | Time: 600 | Output: [{'outputJson': '{"TRoo": 14.99999999999963, "dryBulb": -5.666666666666667, "ZoneSens": 1604.645955026183}'}]
Sim: example-model | Time: 1200 | Output: [{'outputJson': '{"TRoo": 15.00000000000032, "dryBulb": -5.0, "ZoneSens": 1578.976321292014}'}]
Sim: example-model | Time: 1800 | Output: [{'outputJson': '{"TRoo": 15.00000000000019, "dryBulb": -4.333333333333334, "ZoneSens": 1532.971508074938}'}]
Sim: example-model | Time: 2400 | Output: [{'outputJson': '{"TRoo": 15.00000000000001, "dryBulb": -3.666666666666667, "ZoneSens": 1505.238734612665}'}]
Sim: example-model | Time: 3000 | Output: [{'outputJson': '{"TRoo": 15.00000000000032, "dryBulb": -3.0, "ZoneSens": 1476.929963191514}'}]
```

For a full 24-hour (`86400` seconds) simulation, omit `--duration` (or pass `--duration 86400`):

```bash
python run_initialized_model.py example-model
```

### Returned Output Variables

Each time step returns three EnergyPlus `ExternalInterface` output variables in `outputJson`:

| Variable | Description | Unit |
| :--- | :--- | :--- |
| `TRoo` | Zone mean air temperature | `°C` |
| `dryBulb` | Site outdoor air dry-bulb temperature | `°C` |
| `ZoneSens` | Zone sensible heating/cooling rate | `W` |

---

## 5. Direct REST and GraphQL API Examples

You can also interact with the API directly from custom controllers or `curl`.

### Obtain an Auth Token

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/login/ \
  -d "username=user@user.com" \
  -d "password=user user88" | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])")
```

### Query Initialized Models via GraphQL

```bash
curl -s -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "{ fmuModels(modelN: \"example-model\") { modelName stepSize finalTime containerId } }"}'
```

Response:

```json
{
  "data": {
    "fmuModels": [
      {
        "modelName": "example-model",
        "stepSize": 600,
        "finalTime": "24.0",
        "containerId": "simulator"
      }
    ]
  }
}
```

### Send a Time-Step Control Input via REST

```bash
curl -s -X POST http://localhost:8000/input/ \
  -H "Authorization: Token ${TOKEN}" \
  -d "fmu_model=example-model" \
  -d "time_step=3600" \
  -d 'input_json={"time_step": 3600, "yShadeFMU": 0.5}'
```

### Query Time-Step Outputs via GraphQL

```bash
curl -s -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "{ outputs(modelN: \"example-model\", tStep: 0) { timeStep outputJson } }"}'
```

Response:

```json
{
  "data": {
    "outputs": [
      {
        "timeStep": 0,
        "outputJson": "{\"TRoo\": 14.99999999999973, \"dryBulb\": -6.333333333333334, \"ZoneSens\": 1244.017637607269}"
      }
    ]
  }
}
```

---

## 6. Clean Up and Reset

To stop all services and clear database/broker volumes before starting a fresh simulation:

```bash
cd src
docker compose down --volumes
```
