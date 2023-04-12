# Описание

Каталог для материалов практических заданий курса "Школа архитекторов МТС: Базовый".

## Общие правила

- Работы студентов курса ведутся в отдельных репозиториях Github, созданных студентами.
- Каталог для архитектурной документации, создаваемой в ходе выполнения задания, создается на основе содержимого [шаблонного каталога](module_02/README.md).

## Задание

Сквозное [практическое задание](task.md) для выполнения в течение курса.

## Инструменты

Для работы используются следующие инструменты:

- Клиент [Git](https://git-scm.com/) для доступа к Github
- Текстовый редактор (рекомендуется [Visual Studio Code](https://code.visualstudio.com/)).
- Плагины к Visual Studio Code:
  - [vscode-plantuml](https://github.com/qjebbs/vscode-plantuml) - поддержка PlantUML
  - [Markdown All in One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one) – расширенная поддержка Markdown
- Markdown ([Github-диалект Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax))
- [PlantUML](https://plantuml.com/en/):
  - Расширение для С4 диаграмм: https://github.com/plantuml-stdlib/C4-PlantUML
- Дополнительные инструменты, необходимые для выполнения заданий конкретных модулей, указаны в описаниях этих модулей.

### Настройка инструментов

- Для того, чтобы диаграммы PlantUML отображались в режиме Markdown: Preview, необходимо в настройках плагина [vscode-plantuml](https://github.com/qjebbs/vscode-plantuml) установить параметр `plantuml.server` в `https://www.plantuml.com/plantuml`.
- Для поддержки фрагментов кода PlantUML C4 в редакторе, добавьте [файл с ними](https://github.com/plantuml-stdlib/C4-PlantUML/blob/master/.vscode/C4.code-snippets) в папку `<VS Code User Settings Folder>/snippets`.
