#!/bin/bash
set -e

echo '1. Pulling code updates from GitHub...'
git pull

echo '2. Installing project requirements...'
source venv/bin/activate
pip install -r requirements.txt
npm ci --include=dev

echo '3. Building frontend...'
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

echo '4. Collecting static files...'
python manage.py collectstatic --noinput

echo '5. Applying migrations...'
python manage.py migrate --noinput

echo '6. Reloading systemd daemons...'
sudo systemctl reload nginx
sudo systemctl restart burger-store.service

echo '7. Registering deploy on Rollbar...'
ROLLBAR_TOKEN=$(cat .env | grep ROLLBAR_TOKEN | cut -d=   -f2)
REVISION=$(git rev-parse --short HEAD)

curl -s \
     -X POST 'https://api.rollbar.com/api/1/deploy' \
     -H "X-Rollbar-Access-Token: $ROLLBAR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"environment": "production", "revision": "'"$REVISION"'", "rollbar_username": "'"$(whoami)"'", "status": "succeeded"}' \
> /dev/null

echo '8. Deploy completed!'
