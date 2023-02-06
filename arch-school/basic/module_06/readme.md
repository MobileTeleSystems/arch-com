# Description

Демонстрационные материалы к уроку по работе с базами данных и средствами кеширования

```plantuml
@startuml FORIS Текущее состояние

!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

Person(ext_system,"External system")

Boundary(services,"Services"){
    Container( service_author, "Service Author", "python, fastapi, sqlalchemy")
    Container( service_author_cache, "Service Author with Cache", "python, fastapi, sqlalchemy")
    Container( service_presentation, "Service Presentation", "python, fastapi, sqlalchemy")
}

Boundary(dbs,"Databases"){
    ContainerDb( db_node_ex01, "Main SQL database", "MariaDB")
    ContainerDb( cache, "Cache", "Redis")
}

Rel(ext_system,service_author,"http://service_author:8081/authors/{author_id}")
Rel(ext_system,service_author_cache,"http://service_author:8082/authors/{author_id}")
Rel(ext_system,service_presentation,"http://service_author:8083/presentations/{author_id}")

Rel(service_author, db_node_ex01, "Get Author by id","SQL/TCP:3306" )
Rel(service_author, db_node_ex01, "Add Author","SQL/TCP:3306" )
Rel(service_author_cache, db_node_ex01, "Get Author by id","SQL/TCP:3306" )
Rel(service_author_cache, db_node_ex01, "Add Author","SQL/TCP:3306" )
Rel(service_presentation, db_node_ex01, "Get presentations by authors id","SQL/TCP:3306" )
Rel(service_presentation, db_node_ex01, "Add presentations","SQL/TCP:3306" )
Rel(service_author_cache, cache, "Get Author by id","TCP:6379" )
Rel(service_author_cache, cache, "Set Author","TCP:6379" )
@enduml
```

# Python dependances

pip3 install pandas

pip3 install MySQL

pip3 install sqlalchemy

pip3 install PyMySQL

pip3 install "fastapi[all]"

pip3 install "uvicorn[standard]"

pip3 install aioredis 

or

pip3 install -r requirements.txt

# VSCode plugin
Name: MySQL
Id: formulahendry.vscode-mysql
Description: MySQL management tool
Version: 0.4.1
Publisher: Jun Han
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=formulahendry.vscode-mysql

# SQL Alchemy tutorial
https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_declaring_mapping.htm

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