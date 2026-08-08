from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String(10), unique=True, index=True, nullable=True)
    long_url = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    clicks = Column(Integer, default=0)
class Click(Base):
    __tablename__ = "clicks"

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id"))
    timestamp = Column(DateTime, server_default=func.now())
    ip_address = Column(String)    