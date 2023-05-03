from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import json
import os

# Start SQL Alchemy
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_SCHEME = os.getenv('DB_SCHEME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

engine = create_engine("mysql+pymysql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_HOST+":"+DB_PORT+"/"+DB_SCHEME, echo = True)
conn = engine.connect() 

Base = declarative_base()

class Presentation(Base):
   __tablename__ = 'Presentation'
   id = Column(Integer,primary_key=True, index=True)
   title = Column(String)
   author_id = Column(Integer)
   date = Column(Date)


Base.metadata.create_all(engine)

def get_db():
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = Session()
    try:
        yield db
    finally:
        db.close()

# Start FastAPI
app = FastAPI()

def get_presentation_params(db_presentation: Presentation):
    return {
        "id": db_presentation.id,
        "date": db_presentation.date,
        "title": db_presentation.title,
        "author_id": db_presentation.author_id
    }

@app.get("/presentations/{author_id}")
async def read_author(author_id: int, db: Session = Depends(get_db)):
    db_presentation = db.execute("select * from Presentation where author_id = %s" % author_id).fetchall()
    if db_presentation is None or len(db_presentation)==0:
        raise HTTPException(status_code=404, detail="No presentations for this author")

    res =[]
    for dbp in db_presentation:
        res.append(get_presentation_params(dbp))

    return res

@app.post("/presentations")
async def get_body(request: Request, db: Session = Depends(get_db)):
    param_json = await request.json()
    
    db_presentation = Presentation(author_id = param_json['author_id'],
                       title  = param_json['title'],
                       date = param_json['date'])
    db.add(db_presentation)
    db.commit()
    db.refresh(db_presentation)
    return get_presentation_params(db_presentation)

