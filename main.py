from fastapi import FastAPI, Depends, HTTPException, Request, BackgroundTasks
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from models import URL, Click
from schemas import URLCreate, URLResponse
from shortener import encode
from crud import log_click

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/shorten", response_model=URLResponse)
def shorten_url(url_data: URLCreate, db: Session = Depends(get_db)):
    if url_data.custom_alias:
        existing = db.query(URL).filter(URL.short_code == url_data.custom_alias).first()
        if existing:
            raise HTTPException(status_code=409, detail="Alias already taken")

        short_code = url_data.custom_alias
        new_url = URL(long_url=str(url_data.long_url), short_code=short_code)
        db.add(new_url)
        db.commit()
        db.refresh(new_url)

    else:
        new_url = URL(long_url=str(url_data.long_url))
        db.add(new_url)
        db.commit()
        db.refresh(new_url)

        new_url.short_code = encode(new_url.id)
        db.commit()
        db.refresh(new_url)

    return new_url


@app.get("/analytics/{short_code}")
def get_analytics(short_code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")

    clicks = db.query(Click).filter(Click.url_id == url_entry.id).all()

    return {
        "short_code": url_entry.short_code,
        "long_url": url_entry.long_url,
        "clicks": url_entry.clicks,
        "click_details": [{"timestamp": click.timestamp, "ip_address": click.ip_address} for click in clicks]
    }


@app.get("/{short_code}")
def redirect_url(short_code: str, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")

    background_tasks.add_task(log_click, url_entry.id, request.client.host, db)

    return RedirectResponse(url=url_entry.long_url, status_code=302)