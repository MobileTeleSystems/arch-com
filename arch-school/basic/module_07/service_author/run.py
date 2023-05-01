import uvicorn

uvicorn.run("service_author:app", host="127.0.0.1", port=8080, log_level="info")