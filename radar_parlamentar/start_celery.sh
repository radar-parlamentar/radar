export DJANGO_SETTINGS_MODULE=settings.development
celery -A radar_parlamentar worker -l info --concurrency 1
