import subprocess

queue_name = subprocess.getoutput("cat /etc/hostname")

BROKER_URL = 'amqp://user:pass@broker:5672/vhost'
CELERY_RESULT_BACKEND = 'db+postgresql://postgres:backend@backend/backend_db'
CELERY_ROUTES = {'simulator_tasks.*': {'queue': queue_name}}
