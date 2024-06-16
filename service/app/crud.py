from sqlalchemy.orm import Session
from . import models, schemas  # Обратите внимание на точку перед импортами


def get_announcement(db: Session, announcement_id: int):
    return db.query(models.Announcement).filter(models.Announcement.id == announcement_id).first()

def get_announcements(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Announcement).offset(skip).limit(limit).all()

def create_announcement(db: Session, announcement: schemas.AnnouncementCreate):
    db_announcement = models.Announcement(**announcement.dict())
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

def update_announcement(db: Session, announcement_id: int, announcement: schemas.AnnouncementUpdate):
    db_announcement = db.query(models.Announcement).filter(models.Announcement.id == announcement_id).first()
    for key, value in announcement.dict().items():
        setattr(db_announcement, key, value)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

def delete_announcement(db: Session, announcement_id: int):
    db_announcement = db.query(models.Announcement).filter(models.Announcement.id == announcement_id).first()
    db.delete(db_announcement)
    db.commit()
