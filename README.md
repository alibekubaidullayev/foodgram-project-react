# Проект "Foodgram"
Проект "Foodgram" сайт где можно создавать, хранить, искать и делиться рецептами на все случаи жизни.

### Автор:
- [Alibek Ubaidullayev] (https://github.com/alibekubaidullayev)

### Технологии:
- Python
- Django
- DRF
- PostgreSQL
- React


### Как клонировать репозиторий:

Перейдите в любуй папку куда вы хотели бы клонировать репозиторий и наберите следующую комманду:

```
git clone git@github.com:alibekubaidullayev/foodgram-project-react.git
```



### Что внутри .env:

.env файл содержит важную информацию, которую нельзя показывать публично
В нём содержаться следующие поля:
```
DB_ENGINE=django.db.backends.postgresql (бд которую использует Django)
DB_NAME=postgres (название базы данных; postgres - дефолтное значение в postgres)
POSTGRES_USER=postgres (имя пользователя базы данных; postgres - дефолтное значение в postgres)
POSTGRES_PASSWORD=postgres (пароль от базы данных; postgres - дефолтное значение в postgres)
DB_HOST=db (это хост базы данных; если хотите использовать локально то пишете localhost) 
DB_PORT=5432 (порт от который используется pg) 
```


### Как запустить проект локально с помощью докера:

После того как вы клонировали репозиторий (см. выше) выполните слеующие комманды:

Перейти в директорию infra:

```
cd infra
```

Собрать докер контейнера с помощью docker-compose:
```
docker-compose up -d --build
```

Провести миграции:
```
docker-compose exec web python manage.py migrate
```

(При желании) создать суперюзера:
```
docker-compose exec web python manage.py createsuperuser
```

Собрать статику:
```
docker-compose exec web python manage.py collectstatic --no-input 
```


### Как запустить проект локально (без докера):

После того как вы клонировали репозиторий (см. выше) выполните слеующие комманды:

```
cd foodgram
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/Scripts/activate
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
python manage.py migrate
```
Запустить проект на локальной машине:
```
python manage.py runserver
```


### Как открыть сайт локально?:

Сайт откроется на вашем локальном устройстве и будет доступен по ссылке: http://localhost/
redoc: http://localhost/api/docs/
admin: http://localhost/admin/


### Как заполнить базу с помощью фикстур:
После ваполнения миграций выполнить комманду:

Если пользовались Docker:
```
sudo docker-compose exec web python manage.py loaddata fixture.json
```

Если напрямую через Django:
```
python manage.py loaddata fixture.json
```

