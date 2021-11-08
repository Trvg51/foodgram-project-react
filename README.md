# Foodgram
IP - http://51.250.22.172/
```
Для тестов:
Username - admin
Password - Zaq123456
Email - admin@gmail.com
```

Foodgram или «Продуктовый помощник» - Онлайн-сервис и API.
Пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранного».
Реализована возможность скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Развертка проекта в Docker
1. Клонируем репозиторий
```
https://github.com/Trvg51/foodgram-project-react.git
```
2. В папке `backend` с проектом создаем файл `.env` с переменными окружения:
```
SECRET_KEY=django-insecure-p+y(ch7w7zu2*%@mhs+#x7!&khvoi+wdsda&+guc!51$g5l!c8
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
3. В папке `infra` запускаем docker-compose командой
```
docker-compose up
```
Проект запустится на "gunicorn" с базой данных "postgres". Далее с этого терминала ввод комманд станет не доступен, по этому открываем новый терминал.

4. Далее в той же папке `infra` делаем миграции и собираем статику
```
docker-compose exec backend python manage.py makemigrations --noinput
docker-compose exec backend python manage.py migrate --noinput
docker-compose exec backend python manage.py collectstatic --noinput
```
5. Создаем супер-пользователя
```
docker-compose exec backend python manage.py createsuperuser
```
6. Заполняем базу начальными данными (ингредиентами)
```
docker-compose exec backend python manage.py loaddata fixtures/ingredients.json
```
7. Проект доступен по адресу
```
http://127.0.0.1/
```
8. Тэги необходимо добавить через панель администратора
```
http://127.0.0.1/admin/recipes/tag/
```
## Автор
https://github.com/Trvg51