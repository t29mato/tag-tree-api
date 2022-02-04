# Tag Tree API

## Set up Heroku environment

### Environment variables

|KEY|VALUE|NOTE|
|---|--|---|
|DATABASE_URL|******|Generated by Heroku|
|DEBUG|False||
|SECRET_KEY|******|It supposed to be generated by Django|

### Database

```
$ python manage.py migrate
```

## Develop

### Run Server on a local machine

```
$ python manage.py runserver 0.0.0.0:8000
```
