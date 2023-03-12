## Init env
python -m venv env
source env/bin/activate

## Install Flask
https://flask.palletsprojects.com/en/2.2.x/installation/
pip install -U Flask
pip install -U Flask-SQLAlchemy
pip install psycopg2

## Start server (development)
export FLASK_APP=project/__init__.py
export FLASK_DEBUG=1
python manage.py run

## Build Docker image
docker-compose -f docker-compose-dev.yml build
docker-compose -f docker-compose-dev.yml up -d

## Update Docker container
docker-compose -f docker-compose-dev.yml up -d

## Sanity check
docker-compose -f docker-compose-dev.yml up -d --build

## Check logs
docker-compose -f docker-compose-dev.yml logs

## Update permissions to execute script
chmod +x services/users/entrypoint.sh
chmod +x services/users/entrypoint-prod.sh

## Apply model to DB
docker-compose -f docker-compose-dev.yml \
  run users python manage.py recreate-db

## Check in psql
docker exec -ti $(docker ps -aqf "name=users-db") psql -U postgres

\c users_dev
\dt
\q

## Run tests
docker-compose -f docker-compose-dev.yml up -d
docker-compose -f docker-compose-dev.yml \
  run users python manage.py recreate-db
docker-compose -f docker-compose-dev.yml \
  run users python manage.py test

## Runs DB seed
docker-compose -f docker-compose-dev.yml \
  run users python manage.py seed-db

## Check prod settings
docker-compose -f docker-compose-prod.yml run users env

## Rebuild prod
docker-compose -f docker-compose-prod.yml up -d --build


## Update prod
docker-compose -f docker-compose-prod.yml up -d
docker-compose -f docker-compose-prod.yml \
  run users python manage.py recreate-db
docker-compose -f docker-compose-prod.yml \
  run users python manage.py seed-db

## Run Nginx prod container
docker-compose -f docker-compose-prod.yml up -d --build nginx

## Run Nginx dev container
docker-compose -f docker-compose-dev.yml up -d --build nginx

## Run tests
docker-compose -f docker-compose-dev.yml \
  run users python manage.py test

## Init bash profile
source ~/.bashrc

## Docker commands
```sh
// stop containers
docker-compose -f docker-compose-dev.yml stop
//bring down containers
docker-compose -f docker-compose-dev.yml down
// force build
docker-compose -f docker-compose-dev.yml build --no-cache
// remove images
docker rmi $(docker images -q)
// access DB via psql
docker exec -ti users-db psql -U postgres -W
// update containers
docker-compose -f docker-compose-dev.yml up -d
// build containers
docker-compose -f docker-compose-dev.yml up -d --build
// run coverage
docker-compose -f docker-compose-dev.yml \
  run users python manage.py cov
// run linters
docker-compose -f docker-compose-dev.yml \
  run users flake8 project --exclude env
```
