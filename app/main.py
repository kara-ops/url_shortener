from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import JSONResponse
import logging


from sqlalchemy import text
from contextlib import asynccontextmanager
from app.database.postgres import Sessionlocal
from app.database.redis import get_redis
from app.router.auth_routers import router as auth_routers
from app.router.users import router as user_router
from app.router.url_router import router as url_router




@asynccontextmanager
async def lifespan(app:FastAPI):
    try :
        db = Sessionlocal()
        db.execute(text("SELECT 1"))
        db.close()
        print("db working")
    except Exception as e:
        raise RuntimeError(f"Postgress Connection failed {e}")
    
    try :
        redis = get_redis()
        pong = redis.ping()
        print("Redis connection working")
    except Exception as e:
        raise RuntimeError(F"Redis connection failed {e}")
    
    yield

    print("App shuting down")
    


app = FastAPI(lifespan=lifespan)


app.include_router(auth_routers)
app.include_router(user_router)
app.include_router(url_router)

@app.exception_handler(Exception)
async def http_exception_handler(request:Request, exc: HTTPException):
    return JSONResponse(content = {"detail" : exc.detail}, status_code = exc.status_code)

logger = logging.getLogger(__name__)
@app.exception_handler(Exception)
async def generic_exception_handler(request:Request, exc:Exception):
    logger.error(f"Unexpected error:{exc}")
    return JSONResponse(content = {"detail": "Server error"},status_code = 500)