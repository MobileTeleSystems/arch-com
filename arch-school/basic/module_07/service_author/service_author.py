import motor.motor_asyncio
from bson import ObjectId
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Start FastAPI
app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://admin:admin@db-node-ex01/archdb?retryWrites=true&w=majority", authSource="admin")
db = client.college


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class AuthorModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    title: str = Field(...)
    birth_date: str = Field(...)
    birth_year: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "first_name": "Ivan",
                "last_name": "Ivanov",
                "email": "ii@example.com",
                "title": "Title",
                "birth_date": "xxx",
                "birth_year": "yyy",
            }
        }


@app.post("/authors", response_description="Add new Author", response_model=AuthorModel)
async def create_author(author: AuthorModel = Body(...)):
    author = jsonable_encoder(author)
    new_author = await db["authors"].insert_one(author)
    created_author = await db["authors"].find_one({"_id": new_author.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_author)


@app.get("/authors/{author_id}")
async def read_author(author_id: str):
    author = await db["authors"].find_one({"_id": author_id})
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=author)
