from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session


from sql_app import models, schemas, crud
from sql_app.database import SessionLocal, engine
from url_config import CLIENT_URL

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    CLIENT_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_model=list[schemas.Contact])
def read_contacts(db: Session = Depends(get_db)):
    contacts = crud.get_contacts(db)
    return contacts

@app.post("/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = crud.get_contact_by_email(db, email=contact.email)
    if db_contact:
        raise HTTPException(status_code=400, detail="Error! Email already used by another contact.")
    return crud.create_contact(db=db, contact=contact)

@app.put("/", response_model=schemas.Contact)
def edit_contact(contact: schemas.Contact, db: Session = Depends(get_db)):
    db_contact = crud.get_contact_by_id(db, contact_id=contact.contact_id)
    if not db_contact:
        raise HTTPException(status_code=400, detail="Error! Entry not found in database.")
    db_contact = crud.get_contact_by_email_diff_id(db, email = contact.email, contact_id=contact.contact_id)
    if db_contact:
        raise HTTPException(status_code=400, detail="Error! Email already used by another contact.")
    result = crud.edit_contact(db=db, contact=contact)
    return result



@app.delete("/{contact_id}", response_model=list[schemas.Contact])
def delete_contact(contact_id:int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact_by_id(db, contact_id)
    if not db_contact:
        raise HTTPException(status_code=400, detail="Error! Entry not found in database")
    crud.delete_contact(db=db, contact = db_contact)
    contacts = crud.get_contacts(db)
    return contacts