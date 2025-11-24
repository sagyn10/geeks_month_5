#!/bin/sh
set -e

# Ждём, пока БД станет доступна
if [ -z "$DB_HOST" ]; then
  echo "DB_HOST is not set, assuming localhost"
  DB_HOST=localhost
fi

echo "Waiting for postgres at $DB_HOST:$DB_PORT..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 0.5
done

echo "Postgres is up - running migrations"
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

exec "$@"
