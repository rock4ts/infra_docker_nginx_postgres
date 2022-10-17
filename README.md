# API_YaMDb
## Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## Технологии
python 3.7
django 2.2.16
djangorestframework 3.12.4
djangorestframework-simplejwt 5.2.1
## Как запустить проект (OS Windows):

### Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:rock4ts/api_yamdb.git

cd api_yambd
```

### Cоздать и активировать виртуальное окружение:

```
py -3.7 -m venv venv

source venv/Scripts/activate
```
### Обновить pip и установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip

pip install -r requirements.txt
```
### Перейти в директорию, в которой расположен файл manage.py

```
cd api__yambd
```

### Выполнить миграции:

```
python manage.py makemigrations

python manage.py migrate
```
### Запустить проект:

```
python manage.py runserver
```
## Ресурсы API YaMDb
- Ресурс auth: аутентификация.
- Ресурс users: пользователи.
- Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.
## Документация к API проекта APi_YaMDb (v1) доступна по ссылке (после запуска проекта)

http://127.0.0.1:8000/redoc/