## Деплой `prod` версии

1. Перейдите в папку `production`
```sh
cd production
```

2. Создайте и заполните `.env.prod` файл по образцу:

```sh
mv .env.prod.example .env.prod
```

- `SECRET_KEY` — секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на вашем сайте.
- `DEBUG` — дебаг-режим, используйте `False` для деплоя в продакшн
- `ALLOWED_HOSTS` — [см. документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)
- `CSRF_TRUSTED_ORIGINS` – [см. документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#csrf-trusted-origins)
- `YANDEX_APIKEY` — Токен Яндекс API для определения координат по адресу.
- `ROLLBAR_TOKEN` — Токен [Rollbar](rollbar.com) для трекинга ошибок.
- `ROLLBAR_ENVIRONMENT` - Любое удобное название окружения: development, production, stage, test, прочее.  
Для `Postgesql`:
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `POSTGRES_ENGINE`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

3. Запустите деплой скрипт, который:
- Обновит код репозитория
- Соберёт контейнеры
- Подгрузит статику фронтенда
- Зарегистрирует деплой на `rollbar`
- Сообщит об успешном завершении деплоя
- Упадёт в случае ошибки, дальше не пойдёт.
```sh
./deploy.sh
```

4. Создайте и заполните `nginx.conf` файл по образцу.  
В местах, отмеченных комментариями, замените `example.com` на адрес вашего домена
```sh
cp data/nginx/conf.d/nginx.conf.example data/nginx/conf.d/nginx.conf
nano data/nginx/conf.d/nginx.conf
```

5. Запустите скрипт инициализации `certbot`, который:
- загрузит SSL сертификаты от `Let’s Encrypt`
- перезапустит `nginx`
```sh
sudo ./init-letsencrypt.sh
```

6. Накатите миграции
```sh
docker compose -f docker-compose.prod.yaml exec backend python manage.py migrate
```

7. Загрузите тестовые данные: рестораны, блюда, заказы (опционально)
```sh
docker compose -f docker-compose.prod.yaml exec backend python manage.py loaddata data.json
```

8. Создайте учетную запись суперпользователя
```sh
docker compose -f docker-compose.prod.yaml exec backend python manage.py createsuperuser
```

9. Для работы с сервисом используйте следующие ссылки (замените `example.com` на адрес вашего домена):
- главная [https://example.com](https://example.com)
- панель менеджера [https://example.com/manager/orders](https://example.com/manager/orders)
- панель администратора [https://example.com/admin](https://example.com/admin)

