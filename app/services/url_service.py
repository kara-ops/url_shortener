import random, string
from sqlalchemy.orm import Session
from app.models.url_model import Url
from datetime import datetime, timezone, timedelta, tzinfo
from app.services.cache_service import set_url,get_url,increment_click,delete_url_r,get_click_count
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


def get_url_by_code(short_code, db:Session):
    r_check = get_url(short_code) #redis check for url code
    if r_check:
        increment_click(short_code)
        return r_check

    
    p_check = db.query(Url).filter(Url.short_code == short_code).first() #postgres check for code
    if not p_check: #if not in postgres
        raise HTTPException(
            status_code = 404, detail = "Invalid Url"
        )
    activity_check = p_check.is_active #activity check in postgres
    if not activity_check: #if not active
        raise HTTPException(
            status_code = 410, detail = "Url Gone"
        )
    expiry_check = p_check.expires_at.replace(tzinfo=timezone.utc)#expiry check
    if datetime.now(timezone.utc)>expiry_check:
        raise HTTPException(
            status_code = 410, detail = "Url Gone"
        )
    #Set every thing in redis
    ttl = int((expiry_check - datetime.now(timezone.utc)).total_seconds())

    original_url = p_check.original_url
    set_r = set_url(short_code,original_url,ttl)
    increment_click(short_code)
    
    return original_url


def get_user_by_url(db:Session, current_user)->list[Url]:
    p_check = db.query(Url).filter(Url.user_id==current_user).all()
    return p_check

def deactivate_url(db:Session,short_code,current_user):
    p_check = db.query(Url).filter(Url.short_code == short_code).first()
    if not p_check:
        raise HTTPException(
            status_code = 404, detail = "Not found"
        )
   
    if current_user.id != p_check.user_id:
        raise HTTPException(
            status_code = 403, detail = "Not authorized"
        )
    p_check.is_active = False
    db.commit()
    delete_url_r(short_code)
    return p_check

def get_url_stats(short_code,db:Session,current_user):
    in_redis = get_click_count(short_code)
    p_check = db.query(Url).filter(Url.short_code == short_code).first()
    if not p_check:
        raise HTTPException(
            status_code = 404, detail = "Url not found"
        )
    if current_user.id != p_check.user_id:
        raise HTTPException(
            status_code = 403, detail = "No Authentication"
        )
    p_check.click_count = in_redis
    return p_check






    

    
    
           
    
    
    
    




