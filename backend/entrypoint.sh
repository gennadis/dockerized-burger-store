#!/bin/sh
set -e

echo "----- 1. Waiting for Postgres... -----"
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
done
echo "Postgres started."

echo "----- 2. Collecting static files... -----"
python manage.py collectstatic --noinput
echo "Static files collected."

exec "$@"
