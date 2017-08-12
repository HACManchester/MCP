#!/usr/bin/env bash
cd /code

while ! pg_isready -h db -p 5432 > /dev/null 2> /dev/null; do
  echo "Connecting to db Failed"
  sleep 1
done

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
