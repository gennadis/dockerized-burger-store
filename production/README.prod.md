## Деплой `prod` версии

1. Перейдите в папку `production`
```sh
cd production
```

2. Запустите деплой скрипт
```sh
chmod +x deploy.sh
./deploy.sh
```

3. Создайте и заполните `nginx.conf` файл по образцу
В местах, отмеченных комментариями, замените `example.com` на адрес вашего домена
```sh
cp data/nginx/conf.d/nginx.conf.example data/nginx/conf.d/nginx.conf
nano data/nginx/conf.d/nginx.conf
```

4. Запустите скрипт инициализации `certbot`
```sh
chmod +x init-letsencrypt.sh
sudo ./init-letsencrypt.sh
```

5. Накатите миграции
```sh
docker compose -f docker-compose.dev.yaml exec backend python manage.py migrate
```

6. Загрузите тестовые данные (опционально)
```sh
docker compose -f docker-compose.dev.yaml exec backend python manage.py loaddata data.json
```

7. Создайте учетную запись суперпользователя
```sh
docker compose -f docker-compose.dev.yaml exec backend python manage.py createsuperuser
```

8. Для работы с сервисом используйте следующие ссылки (замените `example.com` на адрес вашего домена):
- главная [https://example.com](https://example.com)
- панель менеджера [https://example.com/manager/orders](https://example.com/manager/orders)
- панель администратора [https://example.com/admin](https://example.com/admin)

