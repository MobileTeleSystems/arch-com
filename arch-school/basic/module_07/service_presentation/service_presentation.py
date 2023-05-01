import motor.motor_asyncio
from bson import ObjectId
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

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


class PresentationModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    author_id: str = Field(...)
    date: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Presentation Title",
                "author_id": "xxx",
                "date": "yyy",
            }
        }


@app.get("/presentations/{author_id}")
async def read_presentation(author_id: str):
    cursor = db["presentations"].find({"author_id": author_id})
    if cursor is None:
        raise HTTPException(status_code=404, detail="Presentations not found")
    all_presentations = []
    async for presentation in cursor:
        all_presentations.append(presentation)

    return JSONResponse(status_code=status.HTTP_200_OK, content=list(all_presentations))


@app.post("/presentations", response_description="Add new presentation", response_model=PresentationModel)
async def create_presentation(presentation_body: PresentationModel = Body(...)):
    new_presentation = await db["presentations"].insert_one(jsonable_encoder(presentation_body))
    created_presentation = await db["presentations"].find_one({"_id": new_presentation.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_presentation)

