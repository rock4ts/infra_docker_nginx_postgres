# API_YaMDb
## Описание
Django-проект API YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.<br>
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Добавлять произведения, категории и жанры может только администратор.<br>
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.
<br>

## Технологии
* Python 3.7
* Django 2.2.16
* Django Rest Framework 3.12.4
* Simple JWT 5.2.1
* PostgreSQL 13.0-alpine
* Nginx 1.21.3
* Gunicorn 20.0.4
* Docker 20.10.20
<br>

## Запуск проекта:

__Docker__:

Проект запускается в изолированной среде с помощью системы контейнеризации.
Перед началом работы вам необходимо иметь установленный контейнизатор приложений Docker 19.03.0+.

Проект включает:
- Приложение API,на WSGI-сервере Gunicorn;
- Сервер для  Nginx;
- База данных на основе PostgreSQL.

Каждый сервис запускается в отдельном контейнере.
Dockerfile с конфигурацией образа для контейнера API лежит в папке api_yamdb. Образы PostgreSQL и Nginx автоматически загружаются с DockerHub'a.

__Для запуска проекта:__

Скопируйте репозиторий на локальный компьютер:
```
git clone git@github.com:rock4ts/infra_sp2.git
```

Перейдите в папку с файлом docker-compose.yaml, __все последующие команды выполняйте из этой директории__:
```
cd <project_path>/infra/
```

Перед запуском сборки образов и создания контейнеров, в текущей директории необходимо создать файл .env и указать в нём переменные окружения согласно нижеуказанному примеру:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres # установите свой пароль
DB_HOST=db
DB_PORT=5432

DEBUG=False
```
Для сборки образов и создания контейнеров выполните команду: 
```
docker-compose up -d --build
```
Команда запустит файл docker-compose.yaml, соберёт образы, cоздаст контейнеры для каждого сервиса и свяжет директории с данными медиа-файлов и статики Nginx и API с томами static_value и media_value.

Теперь в контейнере с API (при сборке ему присвоено имя web-yamdb) необходимо выполнить миграции и собрать статику:
```
docker-compose exec web-yamdb python manage.py migrate
```
```
docker-compose exec web-yamdb python manage.py collectstatic --no-input 
```

В директории API-приложения содержится файл fixtures.json с тестовыми данными, для загрузки (по желанию) выполните следующие команды:
```
docker-compose exec web-yamdb python manage.py shell
```
```
# выполнить в открывшемся терминале:
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()
```

```
docker-compose exec web-yamdb python manage.py loaddata fixtures.json
```

Для управления базой данных в админ-зоне создайте суперпользователя:
```
docker-compose exec web-yamdb python manage.py createsuperuser
```
<br>

​Готово! Проект запущен и доступен по адресу [http://127.0.0.1/](http://127.0.0.1/)

#### Примечание:
Проект предусмотривает возможность автоматического заполнения таблиц данными csv-файлов.
Имя файла должно соответствовать названию заполняемой таблицы.
Загружаемые данные должны соответствовать форматам типов соответствующих полей моделей приложения.
Имя файла допускается как в единственном, так и множественном числе.
Для заполнения таблицы из директории `infra/` выполните команду:
```
docker-compose exec web-yamdb python manage.py populate_reviews --path <file_path>/<table_name>.csv
```
<br>

## Ресурсы API YaMDb
- Ресурс auth: аутентификация.
- Ресурс users: пользователи.
- Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.
<br>

__Детальная информация об эндпоинтах и правах доступа к API проекта доступна по ссылке__:
```
http://127.0.0.1/redoc/
```
