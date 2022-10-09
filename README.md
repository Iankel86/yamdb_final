# api_yamdb
![yamdb_final workflow](https://github.com/Iankel86/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
## Групповой проект 
__YAMDB__ собирает отзывы на произведения от пользователей.

ip адрес администрирования сервера: http://62.84.121.242/admin/
Логин - admin
Пароль - admin

Категории произведений: 
- Книги
- Фильмы
- Музыка

Список категорий может быть расширен.
В каждой категории есть произведения: музыкальные, книги или фильмы. Произведению может быть присвоен жанр. Новые жанры может создавать только администратор.
У читателей есть возможность оставлять к произведениям отзывы и выставлять произведению рейтинг.Высчитывается средняя оценка произведения.


## Как установить и запустить проект

- git clone https://github.com/Snowball558/api_yamdb.git
- cd api_final_yatube
- python -m venv venv
- source venv/Scripts/activate
- python -m pip install --upgrade pip
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver


## Примеры запросов
Получение списка всех произведений

__GET /api/v1/titles/__

Получить список всех отзывов к определенному произведению по его id

__GET /api/v1/titles/{title_id}/reviews/__

Получить список всех комментариев к отзыву по id

__GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/__



# api_yamdb

# Описание
Проект **YaMDb** собирает отзывы пользователей на различные произведения. 

При разработке приложения использованы фреймфорки django и django-rest-framework. В качестве базы выступает postgresql Запуск проекта осуществляется средствами docker

# Алгоритм регистрации пользователей
1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
2. **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес  `email`.
3. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле (описание полей — в документации).

# Пользовательские роли
- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь** (`user`) — может, как и **Аноним**, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять **свои** отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- **Модератор** (`moderator`) — те же права, что и у **Аутентифицированного пользователя** плюс право удалять **любые** отзывы и комментарии.
- **Администратор** (`admin`) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям. 
- **Суперюзер Django** — обладет правами администратора (`admin`)


### Регистрация пользователей и выдача токенов
####*Регистрация нового пользователя*

Получить код подтверждения на переданный email.
Права доступа: Доступно без токена.
Использовать имя 'me' в качестве username запрещено.
Поля email и username должны быть уникальными.

POST-запрос ```/api/v1/auth/signup/```:
```
{
  "email": "string",
  "username": "string"
}
```
Пример ответа:
```
{
  "email": "string",
  "username": "string"
}
```
____

####*Получение JWT-токена в обмен на username и confirmation code.*

Права доступа: Доступно без токена.

POST-запрос ```/api/v1/auth/token/```:
```
{
  "username": "string",
  "confirmation_code": "string"
}
```
Пример ответа:
```
{
  "token": "string"
}
```
____
### Категории (типы) произведений
#### *Получение списка всех категорий*

Получить список всех категорий.
Права доступа: Доступно без токена

GET-запрос ```/api/v1/categories/```

Пример ответа:
```
[
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
]
```
____
#### *Добавление новой категории*

Создать категорию.
Права доступа: Администратор.
Поле slug каждой категории должно быть уникальным.

POST-запрос ```/api/v1/categories/```:
```
{
  "name": "string",
  "slug": "string"
}
```
Пример ответа:
```
{
  "name": "string",
  "slug": "string"
}
```
____
#### *Удаление категории*

Удалить категорию.
Права доступа: Администратор.

DELETE-запрос ```/api/v1/categories/{slug}/```:
____
### Категории жанров
#### *Получение списка всех жанров*

Получить список всех жанров.
Права доступа: Доступно без токена

GET-запрос ```/api/v1/genres/```

Пример ответа:
```
[
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
]
```
____
#### *Добавление жанраи*

Добавить жанр.
Права доступа: Администратор.
Поле slug каждого жанра должно быть уникальным.

POST-запрос ```/api/v1/genres/```:
```
{
  "name": "string",
  "slug": "string"
}
```
____
#### *Удаление жанра*

Удалить жанр.
Права доступа: Администратор.

DELETE-запрос ```/api/v1/genres/{slug}/```:
____
### Произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
#### *Получение списка всех произведений*

Получить список всех объектов.
Права доступа: Доступно без токена

GET-запрос ```/api/v1/titles/```

Пример ответа:
```
[
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
]
```
____
#### *Добавление произведения*

Добавить новое произведение.
Права доступа: Администратор.
Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).
При добавлении нового произведения требуется указать уже существующие категорию и жанр.

POST-запрос ```/api/v1/titles/```:
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Пример ответа:
```
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
```
____
#### *Получение информации о произведении*

Информация о произведении.
Права доступа: Доступно без токена

GET-запрос ```/api/v1/titles/{titles_id}/```

Пример ответа:
```
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
```
____
#### *Частичное обновление информации о произведении*

Обновить информацию о произведении
Права доступа: Администратор

PATCH-запрос ```/api/v1/titles/{titles_id}/```:
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Пример ответа:
```
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
```
____
#### *Удаление произведения*

Удалить произведение.
Права доступа: Администратор.

DELETE-запрос ```/api/v1/titles/{titles_id}/```:
____
### Отзывы
#### *Получение списка всех отзывов*

Получить список всех отзывов.
Права доступа: Доступно без токена.

GET-запрос ```/api/v1/titles/{title_id}/reviews/```

Пример ответа:
```
[
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
]
```
____
#### *Добавление нового отзыва*

Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение.
Права доступа: Аутентифицированные пользователи.

POST-запрос ```/api/v1/titles/{title_id}/reviews/```:
```
{
  "text": "string",
  "score": 1
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
____
#### *Полуение отзыва по id*

Получить отзыв по id для указанного произведения.
Права доступа: Доступно без токена.

GET-запрос ```/api/v1/titles/{title_id}/reviews/{review_id}/```

Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
____
#### *Частичное обновление отзыва по id*

Частично обновить отзыв по id.
Права доступа: Автор отзыва, модератор или администратор.

PATCH-запрос ```/api/v1/titles/{title_id}/reviews/{review_id}/```:
```
{
  "text": "string",
  "score": 1
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
____
#### *Удаление отзыва по id*

Удалить отзыв по id.
Права доступа: Автор отзыва, модератор или администратор.

DELETE-запрос ```/api/v1/titles/{title_id}/reviews/{review_id}/```:
____
### Комментарии к отзывам
#### *Получение списка всех комментариев к отзыву*

Получить список всех комментариев к отзыву по id.
Права доступа: Доступно без токена.

GET-запрос ```/api/v1/titles/{title_id}/reviews/{review_id}/comments/```

Пример ответа:
```
[
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
]
```
____
#### *Добавление комментария к отзыву*

Добавить новый комментарий для отзыва.
Права доступа: Аутентифицированные пользователи.

POST-запрос ```/api/v1/titles/{title_id}/reviews/{review_id}/comments/```:
```
{
  "text": "string"
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
____
#### *Получение комментария к отзыву*

Получить комментарий для отзыва по id.
Права доступа: Доступно без токена.

GET-запрос ```/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/```

Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
____
#### *Частичное обновление комментария к отзыву*

Частично обновить комментарий к отзыву по id.
Права доступа: Автор комментария, модератор или администратор.

PATCH-запрос ```/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/```:
```
{
  "text": "string"
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
____
#### *Удаление комментария к отзыву*

Удалить комментарий к отзыву по id.
Права доступа: Автор комментария, модератор или администратор.

DELETE-запрос ```/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/```:
____
### Пользователи
#### *Получение списка всех пользователей*

Получить список всех пользователей.
Права доступа: Администратор

GET-запрос ```/api/v1/users/```

Пример ответа:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
      }
    ]
  }
]
```
____
#### *Добавление пользователя*

Добавить нового пользователя.
Права доступа: Администратор.
Поля email и username должны быть уникальными.

POST-запрос ```/api/v1/users/```:
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
Пример ответа:
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
____
#### *Получение пользователя по username*

Получить пользователя по username.
Права доступа: Администратор.

GET-запрос ```/api/v1/users/{username}/```

Пример ответа:
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
____
#### *Изменение данных пользователя по username*

Изменить данные пользователя по username.
Права доступа: Администратор.
Поля email и username должны быть уникальными.

PATCH-запрос ```/api/v1/users/{username}/```:
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
Пример ответа:
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
____
#### *Удаление пользователя по username*

Удалить пользователя по username.
Права доступа: Администратор.

DELETE-запрос ```/api/v1/users/{username}/```:
____
#### *Получение данных своей учетной записи*

Получить данные своей учетной записи.
Права доступа: Любой авторизованный пользователь

GET-запрос ```/api/v1/users/me/```

Пример ответа:
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
____
#### *Изменение данных своей учетной записи* 

Изменить данные своей учетной записи.
Права доступа: Любой авторизованный пользователь.
Поля email и username должны быть уникальными.

PATCH-запрос ```/api/v1/users/me/```:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}
```
Пример ответа:
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
____

## Установка
```
Пример заполнения .env(должен находиться в каталоге infra):
```
DB_ENGINE=django.db.backends.postgresql

DB_NAME=%имя базы%

POSTGRES_USER=%имя пользователя%

POSTGRES_PASSWORD=%пароль%

DB_HOST=db

DB_PORT=%порт(5432 по умолчанию)%
```
```
Перейти в папку infra и запустить docker-compose.yaml
(при установленном и запущенном Docker)
```
$ cd infra_sp2/infra
$ docker-compose up
```
Для пересборки контейнеров выполнять команду:
(находясь в папке infra, при запущенном Docker)
```
docker-compose up -d --build
```

В контейнере web выполнить миграции:

```
docker-compose exec web python manage.py migrate
```

Создать суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

Собрать статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```

Заполнение бд из файла фикстур:
```
docker exec -it %container_id%  python manage.py shell
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()

docker-compose exec web python manage.py loaddata fixtures.json

```
Проверьте работоспособность приложения, для этого перейдите на страницу:
```
 http://localhost/admin/
```

### Над проектом работали:
- Алексей Аксенов __(Review/Comments)__
https://github.com/Aleksei-Aksenov
- Александр Доведин __(Auth/Users)__
https://github.com/Snowball558
- Ян Шадрин __(Categories/Genres/Titles)__
https://github.com/Iankel86

### В проекте использованы технологии:
- Python
- Django
- Django REST Framework
- Simple JWT
- posgresql
- docker