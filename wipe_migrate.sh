#!/bin/bash
docker-compose stop
docker-compose rm --force
docker-compose run --rm web python manage.py migrate