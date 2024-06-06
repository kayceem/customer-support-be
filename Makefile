# Check unapplied migrations
checkmigrations:
	python manage.py makemigrations --check --no-input --dry-run

# run docker container
up:
	docker-compose -f ./docker-compose.main.yml up

# stop docker containers
down:
	docker-compose down
	
# freeze packages
freeze:
	pip freeze > ./requirements.txt

# make migrations and migrate
migrate:
	python manage.py makemigrations && python manage.py migrate

# run install requirements
requirements:
	pip install --upgrade pip
	pip install -r requirements.txt

# run server 
server: 
	python manage.py runserver

# run server 
server-with-checks: checkmigrations
	python manage.py migrate && python manage.py runserver

# django shell
shell:
	python manage.py shell
	
# create superuser
su:
	python manage.py createsuperuser

# create virtual environment	
venv:
	virtualenv .venv