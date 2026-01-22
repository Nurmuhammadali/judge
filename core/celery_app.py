from celery import Celery

from core.settings import settings

celery_app = Celery(
    "judge",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["apps.tasks.judge_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Import tasks so Celery can discover them
from apps.tasks import judge_tasks  # noqa: F401