# Сайт доставки еды Star Burger

Это сайт сети ресторанов Star Burger. [Здесь](https://gennadis.ru) можно заказать превосходные бургеры с доставкой на дом.

![скриншот сайта](https://dvmn.org/filer/canonical/1594651635/686/)

Сеть Star Burger объединяет несколько ресторанов, действующих под единой франшизой. У всех ресторанов одинаковое меню и одинаковые цены. Просто выберите блюдо из меню на сайте и укажите место доставки. Мы сами найдём ближайший к вам ресторан, всё приготовим и привезём.

На сайте есть три независимых интерфейса. Первый — это публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.

Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. Менеджер видит поступившие новые заказы и первым делом созванивается с клиентом, чтобы подтвердить заказ. После оператор выбирает ближайший ресторан и передаёт туда заказ на исполнение. Там всё приготовят и сами доставят еду клиенту.

Третий интерфейс — это админка. Преимущественно им пользуются программисты при разработке сайта. Также сюда заходит менеджер, чтобы обновить меню ресторанов Star Burger.

## Деплой `dev` версии

1. Клонируйте репозиторий
```sh
git clone https://github.com/gennadis/dockerized-burger-store.git
```

2. Создайте и заполните `.env.dev` файл по образцу
```sh
mv .env.dev.example .env.dev
```

```sh
SECRET_KEY=<secret_key>
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1
YANDEX_APIKEY=<yandex_apikey>
ROLLBAR_TOKEN=<rollbar_token>
ROLLBAR_ENVIRONMENT=dev

POSTGRES_USER=burger_user
POSTGRES_PASSWORD=burger_password
POSTGRES_DB=burger_store
POSTGRES_ENGINE=django.db.backends.postgresql
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

3. Используя `docker compose`, соберите и запустите образы `django`, `parcel` и `postgres`
```sh
docker compose -f docker-compose.dev.yaml up -d --build
```
4. Накатите миграции
```sh
docker compose -f docker-compose.dev.yaml exec backend python manage.py migrate
```
5. Загрузите тестовые данные (опционально)
```sh
docker compose -f docker-compose.dev.yaml exec backend python manage.py loaddata data.json
```
6. Создайте учетную запись суперпользователя
```sh
docker compose -f docker-compose.dev.yaml exec backend python manage.py createsuperuser
```
7. Для работы с сервисом используйте следующие ссылки:
- [главная](http://127.0.0.1:8000)
- [панель менеджера](http://127.0.0.1:8000/manager) 
- [панель администратора](http://127.0.0.1:8000/admin)
