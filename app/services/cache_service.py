from app.database.redis import get_redis
from fastapi import HTTPException

def set_url(short_code, original_url, ttl:int):
    redis = get_redis()
    key = short_code
    redis.setex(key,ttl,original_url)

def get_url(short_code):
    redis = get_redis()
    key = short_code
    return redis.get(short_code)

def delete_url_r(short_code):
    redis = get_redis()
    key = short_code
    redis.delete(key)

def increment_click(short_code):
    redis = get_redis()
    key = short_code
    redis.incr(f"{key}:clicks")

def get_click_count(short_code:str)->int:
    redis = get_redis()
    count =  redis.get(f"{short_code}:clicks")
    return int(count) if count else 0

def rate_limit_redirect(ip:str)->bool:
    redis = get_redis()
    key = f"Redirect:{ip}"
    ttl = 60
    attemps = redis.incr(key)
    if attemps == 1:
        redis.expire(key,ttl)
    if attemps >= 20:
        raise HTTPException(
            status_code = 429, detail = "To many request"
        )
    else:
        return True










