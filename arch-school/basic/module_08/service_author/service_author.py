from fastapi import Depends, FastAPI, HTTPException, Request
import json
from datetime import date

class Author(object):
    '''Class Author'''
    id : int
    first_name : str
    last_name : str
    email : str
    title : str
    birth_date : date
#   birth_year = int
    def __init__(self, id, first_name, last_name, email, title, birth_date):
      self.id = id
      self.first_name = first_name
      self.last_name = last_name
      self.email = email
      self.title = title
      self.birth_date = birth_date
pass

#load data(Authors) from file
json_file_path = "ExportJson.json"  #file path \service_author\\
with open(json_file_path, 'r') as j:
    loadJsonAuthors = json.loads(j.read())
    print(type(loadJsonAuthors))    

    #convert json loadJsonAuthors to python object list of Author
    authors =  []
    for i, val in enumerate(loadJsonAuthors):
        authors.append(Author(**val))


# Start FastAPI
app = FastAPI()

#get Author by id
@app.get("/authors/{author_id}")
async def read_author(author_id: int):
    author =  [val for (it,val) in enumerate(authors) if val.id == author_id]
    
    if author is None : raise HTTPException(status_code=404, detail="No author for this id")
    return author



