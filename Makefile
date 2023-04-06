PORT ?= 8000

dev:
	poetry run flask --app page_analyzer:app run
install:
	poetry install
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

test:
	poetry run pytest

publish:
	poetry publish --dry-run

test-coverage:
	poetry run pytest --cov=hexlet_python_package --cov-report xml

lint:
	poetry run flake8 page_analyzer/app.py

selfcheck:
	poetry check

build:
	poetry build