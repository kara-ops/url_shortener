from celery import Celery
from app.core.config import settings


celery = Celery(
    "url_shortener",
    broker = settings.REDIS_URL,
    backend = settings.REDIS_URL,
    include = ["app.tasks.click_sync"]
)
celery.conf.worker_pool = "solo"

celery.conf.beat_schedule = {
    "sync-clicks-every-hour":{
        "task":"app.tasks.click_sync.sync_click_counts",
        "schedule" : 3600.0,
        
    }
}