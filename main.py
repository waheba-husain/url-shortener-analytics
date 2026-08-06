from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import URL
from schemas import URLCreate, URLResponse
from shortener import encode

app = FastAPI()

@app.post("/shorten", response_model=URLResponse)
def shorten_url(url_data: URLCreate, db: Session = Depends(get_db)):
    if url_data.custom_alias:
        # check if alias is already taken
        existing = db.query(URL).filter(URL.short_code == url_data.custom_alias).first()
        if existing:
            raise HTTPException(status_code=409, detail="Alias already taken")

        short_code = url_data.custom_alias
        new_url = URL(long_url=str(url_data.long_url), short_code=short_code)
        db.add(new_url)
        db.commit()
        db.refresh(new_url)

    else:
        # no alias — create row first to get an auto-generated id
        new_url = URL(long_url=str(url_data.long_url))
        db.add(new_url)
        db.commit()
        db.refresh(new_url)          # now new_url.id exists

        new_url.short_code = encode(new_url.id)
        db.commit()
        db.refresh(new_url)

    return new_url