docker compose -f docker-compose.dev.yaml up -d --build
docker compose -f docker-compose.dev.yaml exec backend python manage.py migrate
docker compose -f docker-compose.dev.yaml exec backend python manage.py loaddata data.json
docker compose -f docker-compose.dev.yaml exec backend python manage.py createsuperuser

http://127.0.0.1:8000
http://127.0.0.1:8000/admin
http://127.0.0.1:8000/manager/orders
