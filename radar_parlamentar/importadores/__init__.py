

# This will make sure the celery app is always imported when
# Django starts so that shared_task will use this app.
from .celery import celery_app