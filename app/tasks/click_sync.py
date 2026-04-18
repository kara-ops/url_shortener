from app.celery_app import celery
from app.database.redis import get_redis
from app.database.postgres import Sessionlocal
from app.models.user_model import User
from app.models.url_model import Url

from app.services.cache_service import get_click_count





@celery.task
def sync_click_counts():
    db = Sessionlocal()
    try:
        p_check = [ row[0] for row in db.query(Url.short_code).all()]
        for sc in p_check:
            code_value = get_click_count(sc)
            if code_value > 0:
                update = db.query(Url).filter(Url.short_code==sc).first()
                update.click_count = code_value
                db.commit()
    
    finally:
        db.close()
           


        



