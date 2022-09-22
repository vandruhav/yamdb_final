# Проект YaMDb_final

## Описание проекта
Проект YaMDb собирает отзывы пользователей на произведения. Произведения
делятся на категории и жанры. Сами произведения в YaMDb не хранятся, здесь
нельзя посмотреть фильм или послушать музыку.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые
отзывы и ставят произведению оценку. Из пользовательских оценок формируется
рейтинг произведения.

В проекте применена технология контейнеризации Docker. Проект состоит из
сервисов, которые запакованы в отдельные контейнеры: Django-приложение, база
данных Postgres, серверы Gunicorn и Nginx. Образ проекта находится на DockerHub,
скачать его можно командой:
```
sudo docker pull vandruhav/api_yamdb:v1
```

## Шаблон env-файла
- SECRET_KEY - ключ к защите подписанных данных
- DEBUG - ключ отладки приложения
- ALLOWED_HOSTS - список хостов/доменов, для которых может работать проект
- DB_ENGINE - используемый движок для доступа к БД
- DB_NAME - имя БД
- POSTGRES_USER - логин для подключения к БД
- POSTGRES_PASSWORD - пароль для подключения к БД
- DB_HOST - название сервиса (контейнера)
- DB_PORT - порт для подключения к БД

## Установка приложения
На вашем компьютере должны быть установлены Docker и надстройка Docker-compose.
1. Склонируйте репозиторий YaMDb с GitHub.com:
```
git clone git@github.com:vandruhav/infra_sp2.git
```
2. Перейдите в директорию:
```
cd infra_sp2/infra
```
3. Соберите контейнеры и запустите их:
```
sudo docker-compose up -d
```
4. Выполните миграции в контейнере web:
```
sudo docker-compose exec web python manage.py migrate
```
5. Создайте суперпользователя в контейнере web:
```
sudo docker-compose exec web python manage.py createsuperuser
```
6. Соберите статику в контейнере web:
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
6. Проект доступен, все функции и эндпойнты описаны в документации:
```
http://localhost/redoc/
```

## Заполнение базы данных
Для заполнения БД данными, предоставленными с проектом, используйте команду:
```
sudo docker-compose exec web python manage.py fill_db
```

## Регистрации пользователей
- Пользователь отправляет POST-запрос на добавление нового пользователя с
параметрами "email" и "username" на эндпойнт "/api/v1/auth/signup/"
- YaMDB отправляет письмо с кодом подтверждения на адрес email.
- Пользователь отправляет POST-запрос с параметрами "username" и
"confirmation_code" на эндпойнт "/api/v1/auth/token/", в ответе на запрос ему
приходит JWT-токен.
- При желании пользователь отправляет PATCH-запрос на эндпойнт
"/api/v1/users/me/" и заполняет поля в своём профайле (описание полей — в
документации).

## Бейдж статуса workflow
[![Django-app workflow](https://github.com/vandruhav/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master)](https://github.com/vandruhav/yamdb_final/actions/workflows/yamdb_workflow.yml)

#
(с) Проект Воробьёва Андрея.
