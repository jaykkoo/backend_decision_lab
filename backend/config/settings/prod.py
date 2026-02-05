from .base import *

DEBUG = False


if os.environ.get("KUBERNETES_SERVICE_HOST"):
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = [
        h.strip()
        for h in os.getenv(
            "DJANGO_ALLOWED_HOSTS",
            "localhost,127.0.0.1"
        ).split(",")
        if h.strip()
    ]

# Sécurité minimale prod
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Logging prod
LOGGING = {
    "version": 1,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}
