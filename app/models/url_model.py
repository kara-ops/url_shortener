from sqlalchemy import Column,Integer,String, ForeignKey, Boolean, DateTime
from datetime import  datetime, timezone
from sqlalchemy.orm import relationship
from app.database.postgres import Base

class Url(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key = True)
    short_code = Column(String, unique = True, nullable = False, index = True)
    original_url = Column(String, nullable = False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    is_active = Column(Boolean, default = True)
    expires_at = Column(DateTime, nullable = False)
    click_count = Column(Integer, default = 0)
    created_at = Column(DateTime, default = lambda : datetime.now(timezone.utc) )


    owner = relationship("User", backref ="urls")