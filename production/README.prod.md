docker compose -f docker-compose.prod.yaml up -d --build
docker compose -f docker-compose.prod.yaml exec backend python manage.py migrate
docker compose -f docker-compose.prod.yaml exec backend python manage.py loaddata data.json
docker compose -f docker-compose.prod.yaml exec backend python manage.py createsuperuser

http://example.com
http://example.com/admin
http://example.com/manager/orders
