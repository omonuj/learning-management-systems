.PHONY: install run migrate makemigrations test lint format check collectstatic

install:
	pip install -r requirements.txt

run:
	python manage.py runserver

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

test:
	python manage.py test --verbosity 2

lint:
	ruff check .

format:
	ruff format .

check:
	python manage.py check

collectstatic:
	python manage.py collectstatic --noinput
