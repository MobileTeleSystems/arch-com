from fastapi import Depends, FastAPI, HTTPException
import requests
from circuitbreaker import circuit, CircuitBreaker
import logging
import threading
import gc
import time

requests.adapters.DEFAULT_RETRIES = 1
circuit_monitor_report_interval_seconds = 1
# service_author = "localhost:8081"
# service_presentation = "localhost:8082"
service_author = "service_author:8081"
service_presentation = "service_presentation:8082"


class Author(object):
    '''Class Author'''
    id: int
    first_name: str
    last_name: str
    email: str
    title: str
    birth_date: str

    def __init__(self, id, first_name, last_name, email, title, birth_date):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.title = title
        self.birth_date = birth_date


class PresentationWithAuthor(object):
    '''Class PresentationWithAuthor'''
    title = str
    last_name: str

    def __init__(self, title, last_name):
        self.title = title
        self.last_name = last_name


class Presentation(object):
    '''Class Presentation'''
    title = str
    author_id = int
    date = str

    def __init__(self, title, author_id, date):
        self.title = title
        self.author_id = author_id
        self.date = date


def author_circuit_exception(*args, **kwargs):
    logging.critical('Circuit OPEN')
    author = Author(0, "temporary unavailable", "temporary unavailable", "temporary unavailable",
                    "temporary unavailable", "temporary unavailable")
    return author


def get_presentation(title):
    response_presentation = requests.get("http://" + service_presentation + "/presentations/" + title)
    presentation = Presentation(**response_presentation.json()[0])
    return presentation


@circuit(failure_threshold=5, recovery_timeout=10, expected_exception=HTTPException,
         fallback_function=author_circuit_exception)
def get_author(id):
    try:
        response_author = requests.get("http://" + service_author + "/authors/" + str(id))
    except requests.exceptions.ConnectionError as errc:
        logging.warning(">>> Error Connecting:", errc)
        raise HTTPException(status_code=500, detail=">>> Error Connecting")
    else:
        author = Author(**response_author.json()[0])
        print(author.last_name)
    return author


# Function to check status of circuit breakers
def circuit_breaker_status():
    while True:
        time.sleep(circuit_monitor_report_interval_seconds)
        for ob in gc.get_objects():
            if isinstance(ob, CircuitBreaker):
                logging.warning(f'Circuit "{ob.name}" is "{ob.state}", failures: {ob.failure_count}')
        logging.warning('')


# Start circuit breaker status check background task
daemon = threading.Thread(target=circuit_breaker_status, daemon=True, name='Monitor')
daemon.start()

# Start FastAPI
app = FastAPI()


@app.get("/presentationsAndAuthor/{title}")
async def read_presentation(title: str):
    presentation = get_presentation(title)
    author = get_author(presentation.author_id)
    presentation_with_author = PresentationWithAuthor(presentation.title, author.last_name)
    return presentation_with_author

# end
