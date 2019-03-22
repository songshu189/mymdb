## MyMDB (My Movie Database), IMDB clone

### Django 2.0, bootstrap 4.0, Postgress, nginx, uWSGI, docker

from **Build Django 2.0 Web Applications**

Replace the environment variables in `.env` file with your real values

DJANGO_ALLOWED_HOSTS is the IP address of your own docker machine, you can get it with
```
$ docker-machine ip default
```
Build the images and start the containers
```
$ docker-compose up -d --build
```
Create super user
```
$ docker exec -it mymdb_web_1 bash -c "cd django; source /mymdb/venv/bin/activate; python manage.py createsuperuser"
```
