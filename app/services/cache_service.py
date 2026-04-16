from app.database.redis import get_redis

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







