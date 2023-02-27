from fastapi import Depends, FastAPI, HTTPException, Request
import requests

class Author(object):
    '''Class Author'''
    id : int
    first_name : str
    last_name : str
    email : str
    title : str
    birth_date : str
    def __init__(self, id, first_name, last_name, email, title, birth_date):
      self.id = id
      self.first_name = first_name
      self.last_name = last_name
      self.email = email
      self.title = title
      self.birth_date = birth_date
pass

class Presentation_With_Author(object):
    '''Class Presentation_With_Author'''    
    title = str
    author = Author
    date = str
    def __init__(self, title, author, date):        
        self.title = title
        self.author = author
        self.date = date
    pass
pass

class Presentation(object):
    '''Class Presentation'''    
    title = str
    author_id = int
    date = str
    def __init__(self, title, author_id, date):        
        self.title = title
        self.author_id = author_id
        self.date = date        
    pass
pass

# Start FastAPI
app = FastAPI()

@app.get("/presentationsAndAuthor/{title}")
async def read_presentation(title: str):
    #get presentation
    responsePresentation = requests.get("/presentations/"+"First Presentation")
    print(responsePresentation)
    if responsePresentation is None : raise HTTPException(status_code=404, detail="No presentations for this id")
    
    #responsePresentation -> presentation
    presentation = Presentation(**responsePresentation.json()[0])
    print(presentation)
    
    #get Author by id 
    responseAuthor = requests.get("/authors/"+str(presentation.author_id))
    print(responseAuthor)
    if responseAuthor is None : raise HTTPException(status_code=404, detail="No presentations for this id")

    #responseAuthor -> author
    author = Author(**responseAuthor.json()[0])

    #new integation class
    presentationWithAuthor = Presentation_With_Author(presentation.title, author, presentation.date)

    return presentationWithAuthor
pass


