# Контекст решения
<!-- Окружение системы (роли, участники, внешние системы) и связи системы с ним. Диаграмма контекста C4 и текстовое описание. 
Подробнее: https://confluence.mts.ru/pages/viewpage.action?pageId=375783261
-->
```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

LAYOUT_WITH_LEGEND()

Person(pbc, "Personal Banking Customer", "A customer of the bank, with personal bank accounts.")
System(ibs, "Internet Banking System", "Allows customers to view information about their bank accounts, and make payments.")
System_Ext(es, "E-mail system", "The internal Microsoft Exchange e-mail system.")
System_Ext(mbs, "Mainframe Banking System", "Stores all of the core banking information about customers, accounts, transactions, etc.")

Rel(pbc, ibs, "Uses")
Rel(es, pbc, "Sends e-mails to")
Rel(ibs, es, "Sends e-mails", "SMTP")
Rel(ibs, mbs, "Uses")
@enduml
```
