from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas  # Обратите внимание на точку перед импортами
from .database import SessionLocal, engine  # Обратите внимание на точку перед database

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/announcements/", response_model=schemas.Announcement)
def create_announcement(announcement: schemas.AnnouncementCreate, db: Session = Depends(get_db)):
    return crud.create_announcement(db=db, announcement=announcement)

@app.get("/announcements/", response_model=list[schemas.Announcement])
def read_announcements(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    announcements = crud.get_announcements(db, skip=skip, limit=limit)
    return announcements

@app.get("/announcements/{announcement_id}", response_model=schemas.Announcement)
def read_announcement(announcement_id: int, db: Session = Depends(get_db)):
    db_announcement = crud.get_announcement(db, announcement_id=announcement_id)
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return db_announcement

@app.put("/announcements/{announcement_id}", response_model=schemas.Announcement)
def update_announcement(announcement_id: int, announcement: schemas.AnnouncementUpdate, db: Session = Depends(get_db)):
    return crud.update_announcement(db=db, announcement_id=announcement_id, announcement=announcement)

@app.delete("/announcements/{announcement_id}")
def delete_announcement(announcement_id: int, db: Session = Depends(get_db)):
    crud.delete_announcement(db=db, announcement_id=announcement_id)
    return {"ok": True}
