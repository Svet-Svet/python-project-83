dev:
	poetry run flask --app page_analyzer:app run
PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
install:
	poetry install

#test: FIXME
#	poetry run pytest

#run: FIXME
#	poetry run page_analyzer

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

test-coverage:
	poetry run pytest --cov=hexlet_python_package --cov-report xml

#lint: FIXME
#	poetry run flake8 page_analyzer/app.py

selfcheck:
	poetry check

build:
	poetry build