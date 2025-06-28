#!/bin/bash

# Charger les variables du fichier .env dans le shell
export $(grep -v '^#' .env | xargs)

docker-compose build
docker-compose up -d


docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Utilisation correcte des variables maintenant disponibles
docker-compose exec -T db mysql -u${DB_USER} -p${DB_PASSWORD} ${DB_NAME} < script1.sql
docker-compose exec -T db mysql -u${DB_USER} -p${DB_PASSWORD} ${DB_NAME} < script2.sql