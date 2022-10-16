Как запустить проект (OS Windows):

Клонировать репозиторий и перейти в него в командной строке:

git clone "ссылка на репозиторий GitHub"

cd api_yambd

Cоздать и активировать виртуальное окружение:

py -3.7 -m venv venv

source venv/Scripts/activate

Обновить pip и установить зависимости из файла requirements.txt:

python -m pip install --upgrade pip

pip install -r requirements.txt

Перейти в директорию, в которой расположен файл manage.py

cd api__yambd

Выполнить миграции:

python manage.py makemigrations

python manage.py migrate

Запустить проект:

python manage.py runserver

Документация к API проекта APi_YAMDB (v1) доступна по ссылке (после запуска проекта)

http://127.0.0.1:8000/redoc/
