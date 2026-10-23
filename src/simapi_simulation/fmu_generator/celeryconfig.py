import os

broker_url = os.getenv("CELERY_BROKER_URL", "amqp://user:pass@broker:5672/vhost")
result_backend = os.getenv(
    "CELERY_RESULT_BACKEND",
    "db+postgresql://postgres:backend@backend/backend_db",
)
task_routes = {"generator_tasks.*": {"queue": "gen"}}
