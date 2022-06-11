cd production

chmod +x deploy.sh
./deploy.sh

nano data/nginx/conf.d/nginx.conf
chmod +x init-letsencrypt.sh
sudo ./init-letsencrypt.sh

docker compose -f docker-compose.prod.yaml exec backend python manage.py migrate
docker compose -f docker-compose.prod.yaml exec backend python manage.py loaddata data.json
docker compose -f docker-compose.prod.yaml exec backend python manage.py createsuperuser

http://example.com
http://example.com/admin
http://example.com/manager/orders
