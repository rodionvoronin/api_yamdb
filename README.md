# API для Yamdb
REST API для плафтормы Yamdb
Проект интерфейса обмена данными для платформой отзывов на произведения искусства Yamdb. С помощью этого интерфейса возможно создание отзывов, их редактирование, добавление комментариев к отзывам, а также оценка произведений и трансляция рейтинга оценок. 

## Используемый стек технологий
- Язык Python
- Фреймворк Django
- Фреймворк Django REST framework
- Язык разметки YAML

## Установка
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:rodionvoronin/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Примеры запросов

Запросы к API начинаются с /api/v1/

### Регистрация нового пользователя

POST /auth/signup/

Request
```
{
  "email": "user@example.com",
  "username": "string"
}
```

Response
```
{
  "email": "string",
  "username": "string"
}
```

### Получение JWT-токена

POST /auth/token/

Request
```
{
  "username": "string",
  "confirmation_code": "string"
}
```

Response
```
{
  "token": "string"
}
```

### Получение списка всех категорий

GET /categories/

Response
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```

### Получение списка всех жанров

GET /genres/

Response
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```

### Получение списка всех произведений

GET /titles/

Response
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```

### Получение списка всех отзывов

GET /titles/{title_id}/reviews/

Response
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

### Получение списка всех комментариев к отзыву

GET /titles/{title_id}/reviews/{review_id}/comments/

Response
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

### Добавление пользователя

POST /users/

Request
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

Response
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```