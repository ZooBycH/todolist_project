graduation project 'todolist'

Учебный дипломный проект - приложение для планирования целей с реализацией:

# Основной стек:

* Python 3.10
* Django 4.1.3
* Postgres

# Подключение зависимостей:
* Менеджер зависимостей **Poetry** 
* `poetry install`

## Функции
1. Аутентификация и пользователь (основное приложение):
   - Аутентификация через ВКонтакте
   - базовая аутентификация Django
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
   - верификация пользователя основного приложения, связывание с аккаунтом телеграмм;
   - просматривать и создание новых целей
   
##  Автоматическая сборка и деплой приложения на сервер:
1. Deploy автоматизирован с github actions. 
2. Используемые файлы проекта:
   - actions**: .github/workflows/actions.yaml
   - compose file: docker-compose-ci.yaml
3. Docker hub images:
   - front: sermalenk/skypro-front:lesson-38
   - back: zoobych/todolist:<tag>
4. Добавить администратора при первом запуске:
   - подключиться к серверу и получить доступ к папке проекта
   - `docker exec -it <api container_id> /bin/bash`
   - `./manage.py createsuperuser`
5. Адреса:
   - front: http://zoobych.ga
   - admin: http://zoobych.ga/admin/
  
   
