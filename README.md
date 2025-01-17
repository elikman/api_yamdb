# Проект YaMDb
Проект **YaMDb** собирает **отзывы (Review)** пользователей на произведения **(Titles)**. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список **категорий (Category)** может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в **YaMDb** не хранятся, здесь нельзя посмотреть фильм или послушать музыку.


### Как запустить проект
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/elikman/api_yamdb.git
```

Cоздать и активировать виртуальное окружение:

Windows
```
python -m venv venv
source venv/Scripts/activate
```
Linux/macOS
```
python3 -m venv venv
source venv/bin/activate
```

Обновить PIP

Windows
```
python -m pip install --upgrade pip
```
Linux/macOS
```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

Windows
```
python manage.py makemigrations
python manage.py migrate
```

Linux/macOS
```
python3 manage.py makemigrations
python3 manage.py migrate
```

Запустить проект:

Windows
```
python manage.py runserver
```

Linux/macOS
```
python3 manage.py runserver
```
Импорт данных из csv:

```
python manage.py load_csv
```

---
## Техническое описание проекта YaMDb

К проекту по адресу `/redoc/` подключена документация API YaMDb. В ней описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.

### Пользовательские роли
**Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
**Аутентифицированный пользователь (user)** — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
**Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
**Администратор (admin)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
**Суперюзер Django** должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

### Самостоятельная регистрация новых пользователей

Пользователь отправляет POST-запрос с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.
После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполнить поля в своём профайле (описание полей — в документации).

### Создание пользователя администратором
Пользователя может создать администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт `api/v1/users/` (описание полей запроса для этого случая — в документации). В этот момент письмо с кодом подтверждения пользователю отправлять не нужно.
После этого пользователь должен самостоятельно отправить свой `email` и `username` на эндпоинт `/api/v1/auth/signup/` , в ответ ему должно прийти письмо с кодом подтверждения.
Далее пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен), как и при самостоятельной регистрации.

## Примеры эндпойтнов

* /api/v1/auth/signup/ (POST): *регистрация нового пользователя.*
* /api/v1/auth/token/ (POST): *получение jwt-токена.*
* /api/v1/categories/ (GET): *Получение списка всех категорий.*
* /api/v1/genres/ (GET, POST): *получение списка всех жанров или создание нового жанра.*
* /api/v1/genres/ (GET, PUT, PATCH, DELETE): *получение, редактирование или удаление произведения.*
* /api/v1/titles/{title_id}/reviews/ (GET): *Получение списка всех отзывов.*
* /api/v1/titles/{title_id}/reviews/ (POST): Добавление нового отзыва*
* /api/v1/titles/{title_id}/reviews/{review_id}/comments/ (GET, POST): *получение списка всех комментариев к отзыву по id или создание нового комментария.*
* /api/v1/users/ (GET): *Получение списка всех пользователей.*

## Примеры ответа от сервера

* POST-запрос: Регистрация нового пользователя. Получить код подтверждения на переданный email.

```
{
    "email": "user@example.com",
    "username": "string"
} 
```

Ответ:

```
{
    "email": "string",
    "username": "string"
}
```

* GET-запрос: Получение списка всех категорий.

Ответ:

```
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
    + {}
    ]
} 

```

* POST-запрос: Добавление произведения.

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

Ответ:

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

### Ресурсы API YaMDb
+ Ресурс **auth**: аутентификация.
+ Ресурс **users**: пользователи.
+ Ресурс **titles**: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
+ Ресурс **categories**: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
+ Ресурс **genres**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
+ Ресурс **reviews**: отзывы на произведения. Отзыв привязан к определённому произведению.
+ Ресурс **comments**: комментарии к отзывам. Комментарий привязан к определённому отзыву.

Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, если это необходимо.

### Связанные данные и каскадное удаление

При удалении объекта пользователя **User** должны удаляться все отзывы и комментарии этого пользователя (вместе с оценками-рейтингами).
При удалении объекта произведения **Title** должны удаляться все отзывы к этому произведению и комментарии к ним.
При удалении объекта отзыва **Review** должны быть удалены все комментарии к этому отзыву.
При удалении объекта категории **Category** не нужно удалять связанные с этой категорией произведения.
При удалении объекта жанра **Genre** не нужно удалять связанные с этим жанром произведения.

# Авторы
[Набиев Эльтадж](https://github.com/elikman)
