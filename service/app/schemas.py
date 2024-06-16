from pydantic import BaseModel

class AnnouncementBase(BaseModel):
    title: str
    content: str

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(AnnouncementBase):
    pass

class Announcement(AnnouncementBase):
    id: int

    class Config:
        orm_mode = True
