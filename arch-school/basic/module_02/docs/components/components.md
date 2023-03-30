# Компонентная архитектура
<!-- Состав и взаимосвязи компонентов системы между собой и внешними системами с указанием протоколов, ключевые технологии, используемые для реализации компонентов.
Диаграмма контейнеров C4 и текстовое описание. 
Подробнее: https://confluence.mts.ru/pages/viewpage.action?pageId=375783368
-->
## Контейнерная диаграмма

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

AddElementTag("microService", $shape=EightSidedShape(), $bgColor="CornflowerBlue", $fontColor="white", $legendText="microservice")
AddElementTag("storage", $shape=RoundedBoxShape(), $bgColor="lightSkyBlue", $fontColor="white")

Person(customer, "Покупатель", "B2C клиент")

System_Boundary(c, "MTS Shop Lite") {
   Container(app, "Клиентское веб-приложение", "html, JavaScript, Angular", "Портал интернет-магазина")
   Container(offering_service, "Product Offering Service", "Java, Spring Boot", "Сервис управления продуктовым предложением", $tags = "microService")      
   ContainerDb(offering_db, "Product Catalog", "PostgreSQL", "Хранение продуктовых предложений", $tags = "storage")
   
   Container(ordering_service, "Product Ordering Service", "Golang, nginx", "Сервис управления заказом", $tags = "microService")      
   ContainerDb(ordering_db, "Order Inventory", "MySQL", "Хранение заказов", $tags = "storage")
    
   Container(message_bus, "Message Bus", "RabbitMQ", "Транспорт для бизнес-событий")
   Container(audit_service, "Audit Service", "C#/.NET", "Сервис аудита", $tags = "microService")      
   Container(audit_store, "Audit Store", "Event Store", "Хранение произошедших события для аудита", $tags = "storage")
}

System_Ext(logistics_system, "msLogistix", "Система управления доставкой товаров.")  

Lay_R(offering_service, ordering_service)
Lay_R(offering_service, logistics_system)
Lay_D(offering_service, audit_service)

Rel(customer, app, "Оформление заказа", "HTTPS")
Rel(app, offering_service, "Выбор продуктов для корзины(Продукт):корзина", "JSON, HTTPS")

Rel(offering_service, message_bus, "Отправка заказа(Корзина)", "AMPQ")
Rel(offering_service, offering_db, "Сохранение продуктового предложения(Продуктовая спецификация)", "JDBC, SQL")

Rel(ordering_service, message_bus, "Получение заказа: Корзина", "AMPQ")
Rel_U(audit_service, message_bus, "Получение события аудита(Событие)", "AMPQ")

Rel(ordering_service, ordering_db, "Сохранение заказа(Заказ)", "SQL")
Rel(audit_service, audit_store, "Сохранение события(Событие)")
Rel(ordering_service, logistics_system, "Доставка(Наряд на доставку):Трекинг", "JSON, HTTP")  

SHOW_LEGEND()
@enduml
```

## Список компонентов
| Компонент             | Роль/назначение                  |
|:----------------------|:---------------------------------|
| *Название компонента* | *Описание назначения компонента* |