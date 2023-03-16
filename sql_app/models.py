from sqlalchemy import Column, String, Integer

from .database import Base

class Contact(Base):
    __tablename__ = "contact_table"
    contact_id = Column(Integer, primary_key=True, index = True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)