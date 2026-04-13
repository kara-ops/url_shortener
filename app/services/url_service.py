import random, string
from sqlalchemy.orm import Session
from app.models.url_model import Url
from datetime import datetime, timezone, timedelta
from app.services.cache_service import set_url
from fastapi import HTTPException
from app.schemas.url_schema import URLCreate

def generate_short_code():
    result = ''.join(random.choices(string.ascii_letters + string.digits, k = 6))
    return result

def create_url(db:Session,original_url,current_user)->Url:
    code = 0
    while True:
       code = generate_short_code()
       check_db= db.query(Url).filter(Url.short_code == code).first()
       if not check_db:
           break
       
    ttl = 60*60*24*7
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    
    new_url = Url(
        short_code = code,
        expires_at = expires_at, 
        original_url = original_url,
        user_id  = current_user.id
        )
    # try:
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    set_url(code, original_url, ttl)
    # except Exception as e:
    #     db.rollback()
    #     raise HTTPException(
    #         status_code = 500, detail = "Failed to create a url"
    #     )

    return new_url




    

    
    
           
    
    
    
    




