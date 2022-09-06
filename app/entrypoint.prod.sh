#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "Starting makemigrations"
python manage.py flush --no-input
python manage.py makemigrations
python manage.py collectstatic --no-input
echo "Finished makemigrations"

echo "Starting migrate"
python manage.py migrate
echo "Finished migrate"

python -m spacy download en_core_web_md

#echo "Starting Rasa Train model"
rasa train
#echo "Finised Rasa Train"

rasa run -m models --enable-api --cors "*" & rasa run actions &

exec "$@"