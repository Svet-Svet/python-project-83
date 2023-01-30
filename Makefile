dev:
	poetry run flask --app page_analyzer:app run
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

lint:
	poetry run flake8 page_analyzer/app.py

selfcheck:
	poetry check

build:
	poetry build