# Модуль 4
Пример интеграционного сервиса
<br>


## Установка
* Устанавливаем docker. https://docs.docker.com/desktop/install/windows-install/

* Устанавливаем питон pip - pip install "uvicorn[standard]"
* Устанавливаем фреймворк для запуска сервисов fastapi - pip install fastapi
* Устанавливаем дополнения - pip install requests
* Устанавливаем дополнения - pip install uvicorn
* Устанавливаем дополнения - pip install pyyaml
* Обновляем питон - python.exe -m pip install --upgrade pip


Забираете с GIT module_04 

* Запуск серввисов локально - uvicorn service_presentation:app --reload 

В директории module_04 запускаем - docker-compose build && docker-compose up -d

* Обращаемся к сервису презентаций - http://127.0.0.1:8082/presentations/Second%20Presentation

* Обращаемся к сервису авторов - http://127.0.0.1:8081/authors/1

* Обращаемся к интеграционному сервису - http://127.0.0.1:8083/presentationsAndAuthor/First%20Presentation

