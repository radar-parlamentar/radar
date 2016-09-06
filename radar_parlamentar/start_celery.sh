export DJANGO_SETTINGS_MODULE=settings.development
celery -A importadores worker -l info --concurrency 1

