from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import aioredis
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

class Author(Base):
   __tablename__ = 'Author'
   id = Column(Integer,primary_key=True, index=True)
   first_name = Column(String)
   last_name = Column(String)
   email = Column(String)
   title = Column(String)
   birth_date = Column(Date)
   birth_year = Column(Integer)  

Base.metadata.create_all(engine)

def get_db():
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = Session()
    try:
        yield db
    finally:
        db.close()

# Connect to Redis
redis = aioredis.from_url("redis://cache:6379", decode_responses=True)

# Start FastAPI
app = FastAPI()

def get_author_params(db_author: Author):
    return {
        "id": db_author.id,
        "birth_date": db_author.birth_date,
        "birth_year": db_author.birth_year,
        "title": db_author.title,
        "email": db_author.email,
        "first_name": db_author.first_name,
        "last_name": db_author.last_name,
    }

# using cache
@app.get("/authors/{author_id}")
async def read_author_cache(author_id: int, db: Session = Depends(get_db)):
    redis_result = await redis.get(str(author_id))
    if redis_result:
        return json.loads(redis_result)

    db_author = db.execute("select * from Author where id = %s" % author_id).first()

    if db_author is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        await redis.set(str(author_id), json.dumps(get_author_params(db_author)))

    return get_author_params(db_author)

@app.post("/authors")
async def get_body(request: Request, db: Session = Depends(get_db)):
    param_json = await request.json()
    redis_result = await redis.get(str(author_id))
    
    db_author = Author(first_name = param_json['first_name'],
                       last_name  = param_json['last_name'],
                       email = param_json['email'],
                       title = param_json['title'],
                       birth_date = param_json['birth_date'],
                       birth_year = param_json['birth_year'])
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    await redis.set(str(author_id), json.dumps(get_author_params(db_author)))

    return get_author_params(db_author)