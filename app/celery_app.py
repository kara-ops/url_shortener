from celery import Celery


celery = Celery(
    "url_shortener",
    broker = "redis://localhost:6379/0",
    backend = "redis://localhost:6379/0",
    include = ["app.tasks.click_sync"]
)
celery.conf.worker_pool = "solo"

celery.conf.beat_schedule = {
    "sync-clicks-every-hour":{
        "task":"app.tasks.click_sync.sync_click_counts",
        "schedule" : 3600.0,
        
    }
}