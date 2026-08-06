from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl


class URLBase(BaseModel):
    long_url: HttpUrl
    custom_alias: Optional[str] = None


class URLCreate(URLBase):
    pass


class URLResponse(URLBase):
    id: int
    short_code: str
    created_at: Optional[datetime] = None
    clicks: int

    class Config:
        orm_mode = True
