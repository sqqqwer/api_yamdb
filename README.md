# API-YAMDB
API реализация проекта "YAMDB"

# Функционал
- Реализована система регистрации и аутентификации пользователей
- Произведения могут создавать только администраторы проекта
- Авторизованные пользователи могут оставлять отзывы к произведениям
- Авторизованные пользователи могут оставлять комментарии к отзывам

## Как импортировать данные из .csv документов:
1. Находясь в директории api_yamdb/ cоздайте базу данных.
'''shell
    python manage.py migrate
'''
2. Запустите импортёр.
'''shell
    python manage.py loadfromcsv 'd:/Dev/api_yamdb/api_yamdb/static/data'
'''
... to be continued