from .base import *

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost" ,"django",]


# Logging simple
LOGGING = {
    "version": 1,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

CELERY_BROKER_URL = "amqp://guest:guest@rabbitmq:5672//"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

API_BASE_URL = "http://django:8000/api/v1"
REDIS_URL="redis://redis:6379/"