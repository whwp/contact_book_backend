
from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models, schemas
from sql_app import models, schemas

def get_contacts(db: Session):
    return db.query(models.Contact).all()

def get_contact_by_email(db: Session, email: str):
    return db.query(models.Contact).filter(models.Contact.email == email).first()

def get_contact_by_id(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.contact_id == contact_id).first()
    
"""search the contact with the same email but different contact_id"""
def get_contact_by_email_diff_id(db: Session, email: str, contact_id: int):
    return db.query(models.Contact).filter(
        and_(models.Contact.email == email, models.Contact.contact_id != contact_id)
        ).first()

def delete_contact_by_id(db: Session, contact_id: str):
    db_contact = db.query(models.Contact).filter(models.Contact.contact_id == contact_id).first()
    db.delete(db_contact)
    db.commit()
    return {"ok": True}

def delete_contact(db: Session, contact: models.Contact):
    db.delete(contact)
    db.commit()

def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(first_name = contact.first_name, last_name = contact.last_name, email=contact.email)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def edit_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = db.get(models.Contact, contact.contact_id)
    db_contact.first_name = contact.first_name
    db_contact.last_name = contact.last_name
    db_contact.email = contact.email
    db.commit()
    db.refresh(db_contact)
    return db_contact