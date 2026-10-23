broker_url = "amqp://user:pass@broker:5672/vhost"
result_backend = "db+postgresql://postgres:backend@backend/backend_db"
task_routes = {"generator_tasks.*": {"queue": "gen"}}
