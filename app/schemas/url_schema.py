from pydantic import BaseModel,ConfigDict,AnyHttpUrl
from datetime import datetime




class URLCreate(BaseModel):
    original_url : str


class URLResponse(BaseModel):
    original_url : str
    short_code : str
    expires_at : datetime
    created_at : datetime
    
    model_config = ConfigDict(from_attributes = True)


class URLStatsResponse(BaseModel):
    expires_at : datetime
    created_at : datetime
    click_count : int
    model_config = ConfigDict(from_attributes = True)









    


