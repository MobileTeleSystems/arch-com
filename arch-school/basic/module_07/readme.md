# Description

Демонстрационные материалы к уроку по работе с базами данных и средствами кеширования

**Warning!**
Необходимо использовать версию python не выше 3.9. На более новых выдает ошибку  
```
ImportError: cannot import name 'coroutine' from 'asyncio' (/usr/local/Cellar/python@3.11/3.11.3/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/__init__.py)
```


```plantuml
@startuml FORIS Текущее состояние

!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

Person(ext_system,"External system")

Boundary(services,"Services"){
    Container( service_author, "Service Author", "python, fastapi")
    Container( service_author_cache, "Service Author with Cache", "python, fastapi")
    Container( service_presentation, "Service Presentation", "python, fastapi")
}

Boundary(dbs,"Databases"){
    ContainerDb( db_node_ex01, "Main database", "MongoDb")
    ContainerDb( cache, "Cache", "Redis")
}

Rel(ext_system,service_author,"http://service_author:8081/authors/{author_id}")
Rel(ext_system,service_author_cache,"http://service_author:8082/authors/{author_id}")
Rel(ext_system,service_presentation,"http://service_author:8083/presentations/{author_id}")

Rel(service_author, db_node_ex01, "Get Author by id","TCP:27017" )
Rel(service_author, db_node_ex01, "Add Author","TCP:27017" )
Rel(service_author_cache, db_node_ex01, "Get Author by id","TCP:27017" )
Rel(service_author_cache, db_node_ex01, "Add Author","TCP:27017" )
Rel(service_presentation, db_node_ex01, "Get presentations by authors id","TCP:27017" )
Rel(service_presentation, db_node_ex01, "Add presentations","TCP:27017" )
Rel(service_author_cache, cache, "Get Author by id","TCP:6379" )
Rel(service_author_cache, cache, "Set Author","TCP:6379" )
@enduml
```

# Python dependencies

pip3 install -r requirements.txt

# FastAPI tutorial
https://fastapi.tiangolo.com/tutorial/

# AIO Redis tutorial
https://aioredis.readthedocs.io/en/latest/getting-started/


# Run examples
## Run from external (not corporate) network
docker-compose pull
## Start
docker-compose up

# Performance test
## Without cache
wrk -d 10 -t 10 -c 10 --latency -s ./get.lua http://localhost:8081/
## With cache
wrk -d 10 -t 10 -c 10 --latency -s ./get.lua http://localhost:8082/
