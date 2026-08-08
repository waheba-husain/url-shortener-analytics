from sqlalchemy.orm import Session
from models import URL, Click

def log_click(url_id: int, ip_address: str, db: Session):
    click = Click(url_id=url_id, ip_address=ip_address)
    db.add(click)

    url = db.query(URL).filter(URL.id == url_id).first()
    if url:
        url.clicks += 1

    db.commit()