from pydantic import BaseModel

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    contact_id: int

    class Config:
        orm_mode = True