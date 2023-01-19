graduation project 'todolist'

Учебный дипломный проект - приложение для планирования целей с реализацией:

# Основной стек:

* Python 3.10
* Django 4.1.3
* Postgres

# Подключение зависимостей:
* Менеджер зависимостей **Poetry** 
* `poetry install`

### Функции
1. Аутентификация и пользователь (основное приложение):
   - ВК Оаут `(в разработке)`
   - базовая аутентификация джанго
   - обновление профиля
   - изменение пароля
2.Основной интерфейс (приложение целей):
   - базовый CRUD с фильтрами и сортировкой: доски, цели, категории, комментарии
   - пользователь может просматривать элементы, связанные с досками, членом которых он является (владелец, писатель или читатель)
   - пользователь может создавать категории, цели, комментарии, только если он является владельцем/автором соответствующей доски
   - пользователь может обновлять, удалять, только если он является владельцем/писателем соответствующей доски
   - пользователь может обновлять, удалять только свои комментарии
   - когда доска, категория отмечена как is_deleted, все дочерние категории, цели также отмечены как is_deleted
3. Бот Telegram (бот-приложение):
   - пользователю необходимо подтвердить личность с помощью кода подтверждения
   - пользователь мог просматривать и создавать цели
   - имя пользователя в телеграмме бота: `(в разработке)`
   
