from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session
from app.services import url_service
from app.schemas.url_schema import URLCreate,URLResponse, URLRedirect,RedirectRequest
from app.database import postgres
from app.core.dependencies import get_current_user


router = APIRouter(prefix = "/urls", tags = ["urls"])

@router.post("/", response_model = URLResponse )
def create_url(request:URLCreate, db:Session = Depends(postgres.get_db),current_user:dict = Depends(get_current_user)):
    create_it = url_service.create_url(db,request.original_url,current_user)
    return create_it

@router.get("/")
def redirect_url(request:RedirectRequest, db : Session = Depends(postgres.get_db)):
    check = url_service.get_url_by_code(request.short_code,db)
    return URLRedirect(original_url = check)


