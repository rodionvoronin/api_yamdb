Проект «API для Yatube»


Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

git clone https://github.com/sarafantofun/api_final_yatube.git
cd api_final_yatube
Cоздать и активировать виртуальное окружение:

python -m venv venv
source venv/scripts/activate
Установить зависимости из файла requirements.txt:

python -m pip install --upgrade pip
pip install -r requirements.txt
Выполнить миграции:

python manage.py migrate
Запустить проект:

python manage.py runserver

Примеры запросов к API:
http://127.0.0.1:8000/redoc/