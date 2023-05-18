from fastapi import Depends, FastAPI, HTTPException, Request
import json
from datetime import date

class Presentation(object):
    '''Class Presentation'''    
    title = str
    author_id = int
    date = date
    def __init__(self, title, author_id, date):        
        self.title = title
        self.author_id = author_id
        self.date = date        
    pass
pass

#get data from file 
json_file_path = "ExportJsonPresentation.json" #dir for file \service_presentation\\
with open(json_file_path, 'r') as j:
    loadJsonPresentations = json.loads(j.read())
    print(type(loadJsonPresentations))

    #convert json loadJsonPresentations to python object list of Presentation
    presentations =  []
    for i, val in enumerate(loadJsonPresentations):
        presentations.append(Presentation(**val))

# Start FastAPI
app = FastAPI()

#test api
#@app.get("/")
#async def homepage():
#   return {"Hello": "World"}

#API get by title
@app.get("/presentations/{title}")
async def read_presentation(title: str):
    presentation = [val for (it,val) in enumerate(presentations) if val.title == title]
    if presentation is None : raise HTTPException(status_code=404, detail="No presentations for this id")
    return presentation

#get All presenation    
@app.get("/presentations")
async def get_all_presentations():
    return presentations

