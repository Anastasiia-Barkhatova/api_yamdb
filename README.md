### **YaMDb**

> Проект собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся. Произведения делятся на категории, им может быть присвоен жанр из списка предустановленных. Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку, из пользовательских оценок формируется рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв. Пользователи могут оставлять комментарии к отзывам.

### **Cтек технологий:**
- Python 3.9
- Django 3.2.16
- Django Rest Framework 3.12.4
- SQLite3

### **Как запустить проект:**

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/Anastasiia-Barkhatova/api_yamdb
```

```bash
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

Обновить pip

```bash
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

Перейти в репозиторий api_yamdb

```bash
cd api_yamdb
```

Выполнить миграции:

```bash
python manage.py migrate
```

Запустить проект на сервере:

```bash
python manage.py runserver
```

### **Заливка данных из файлов .csv в базу данных:**

Перейти в репозиторий api_yamdb

```bash
cd api_yamdb
```
Для заливки всех файлов директории \api_yamdb\static\data выполните команду:

```bash
python manage.py upload_data write
```
Для заливки отдельного файла выполните команду:

```bash
python manage.py upload_data write -F <имя_файла>
```
или команду:

```bash
python manage.py upload_data write --file_name <имя_файла>
```

### **Примеры запросов к API:**

* Пример GET-запроса для получения списка всех произведений, к которым пишут отзывы:
```
...api/v1/titles/
```
* Пример ответа:
```
[
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "^-$"
        }
      ],
      "category": {
        "name": "string",
        "slug": "^-$"
      }
    }
  ]

```
* Пример GET-запроса для получения списка всех отзывов:
```
...api/v1/titles/{title_id}/reviews/
```
* Пример ответа:
```
[
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
    {
      "id": 1,
      "text": "string",
      "author": "string",
      "score": 10,
      "pub_date": "2022-09-24T14:15:22Z"
    }
  ]

```

* Пример POST-запроса для добавления отзыва:
```
...api/v1/titles/{title_id}/reviews/
```
```
{
  "text": "string",
  "score": 1
}
```
* Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}

```

* Пример POST-запроса для добавления комментария к отзыву:
```
...api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
```
{
  "text": "string"
}
```
* Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
* Пример GET-запроса для получения списка всех пользователей:
```
...api/v1/users/
```
* Пример ответа:
```
[
    {
      "username": "^w\\Z",
      "email": "user@example.com",
      "first_name": "string",
      "last_name": "string",
      "bio": "string",
      "role": "user"
    }
  ]
```
[Посмотреть примеры других запросов](http://127.0.0.1:8000/redoc/)


Авторы: [Васин Виктор](https://github.com/BinDigMind), [Караськин Максим](https://github.com/mac7simka), [Бархатова Анастасия](https://github.com/Anastasiia-Barkhatova)
