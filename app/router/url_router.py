from fastapi import APIRouter, HTTPException,Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.services import url_service, cache_service
from app.schemas.url_schema import URLCreate,URLResponse, URLStatsResponse
from app.database import postgres
from app.core.dependencies import get_current_user


router = APIRouter(prefix = "/urls", tags = ["urls"])

@router.post("/", response_model = URLResponse )
def create_url(request:URLCreate, db:Session = Depends(postgres.get_db),current_user:dict = Depends(get_current_user)):
    create_it = url_service.create_url(db,request.original_url,current_user)
    return create_it

@router.get("/{short_code}")
def redirect_url( request:Request,short_code : str, db : Session = Depends(postgres.get_db)):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.client.host
    call = cache_service.rate_limit_redirect(ip)
    check = url_service.get_url_by_code(short_code,db)
    return RedirectResponse(url=check,status_code = 302)

@router.get("/", response_model = list[URLResponse])
def get_user_url(current_user:dict = Depends(get_current_user),db: Session = Depends(postgres.get_db)):
    check = url_service.get_user_by_url(db,current_user.id)
    return check

@router.delete("/{short_code}",status_code = 200)
def delete_url(short_code : str,db:Session = Depends(postgres.get_db),current_user : dict = Depends(get_current_user)):
    check = url_service.deactivate_url(db,short_code,current_user)
    return {"message" : "Url deactivated"}


@router.get("/{short_code}/stats",response_model = URLStatsResponse)
def  get_url_stats(short_code : str,db:Session = Depends(postgres.get_db), current_user:dict=Depends(get_current_user)):
    check = url_service.get_url_stats(short_code,db,current_user)
    return check
    
#cOAB9P 