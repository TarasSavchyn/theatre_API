# API_Theatre

Our project is an innovative theater management system that simplifies and optimizes all aspects of theater life, 
starting from the organization of the performance and ending with the form of free seats and ratings of the performance. 
The main functions of the system include:
- Play and Actor: Detailed information about plays, including titles, descriptions, genres, and actors involved. Actors 
also have their own profiles with pictures.

- Performance: The system allows you to easily add and manage performances and screenings in different theater halls, i
ncluding information about times and seat availability.

- Reservation : Users can reserve tickets for their desired shows and performances. The system keeps track of reserved 
seats and their status.

- Ratings : Users can leave ratings and reviews of performances, and the system calculates an average rating for all performances.

- Theater Halls: Detailed information about theater halls, including the number of rows and seats in each.

- Automatic Rating Update: Show ratings are automatically updated based on user feedback.

Our system helps theaters manage their activities efficiently, attract new audiences and provide a convenient way to reserve tickets. .

## сontent
- [technology](#technology)
- [testing](#testing)
- [docker](#docker)
- [using](#using)
- [project developer](#project-developer)

## technology
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django-Rest-Framework](https://www.django-rest-framework.org/)
- [Swagger](https://swagger.io/)
- [Django-Debug-Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#process)
- [Docker](https://www.docker.com/)
- [TestCase](https://docs.djangoproject.com/en/4.2/topics/testing/tools/)

## Using
Clone the repository from GitHub:
```sh
$ git clone https://github.com/TarasSavchyn/theatre_API.git
```
Once you've cloned the repository, navigate into the repository.

Create a virtual environment and activate it using the following commands:
```sh
$ python3 -m venv venv
$ source venv/bin/activate
```
Once you've activated your virtual environment install your python packages by running:
```sh
$ pip install -r requirements.txt
```
Now let's migrate our django project:
```sh
$ python3 manage.py migrate
```
If there are no hitches here you should now be able to open your server by running:
```sh
$ python3 manage.py runserver
```
Go to the web browser and enter http://127.0.0.1:8000/api/theatre/


## Docker
Create file ".env" with the following content:
```python
POSTGRES_ENGINE=POSTGRES_ENGINE
POSTGRES_NAME=POSTGRES_NAME
POSTGRES_USER=POSTGRES_USER
POSTGRES_PASSWORD=POSTGRES_PASSWORD
POSTGRES_HOST=POSTGRES_HOST
POSTGRES_PORT=POSTGRES_PORT
```
After that create the file "docker-compose.yml"
```python
version: '3'
services:
  web:
    image: savik1992/theatre-app:latest
    container_name: theatre-container
    ports:
      - "8000:8000"
    command: ["python", "manage.py", "runserver", "0.0.0.0:8000"]
    working_dir: /app
    depends_on:
      - db
  db:
    image: postgres:latest
    container_name: theatre-postgres-container
    env_file:
      - .env
    ports:
      - "5433:5432"
```
Then open your terminal and navigate to the directory you wish to store the project and run the following commands:
```sh
$ docker push savik1992/theatre-app
$ docker-compose up
```
Welcome, the application is ready to use at url http://127.0.0.1:8000/admin/theatre/

## Testing

Unittest was used to test the project. To run the tests, execute:
```sh
$ python3 manage.py test 
```

## Project developer

- [Taras Savchyn](https://www.linkedin.com/in/%D1%82%D0%B0%D1%80%D0%B0%D1%81-%D1%81%D0%B0%D0%B2%D1%87%D0%B8%D0%BD-ba2705261/) — Python Developer
