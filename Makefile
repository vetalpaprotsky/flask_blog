run:
	FLASK_APP=run.py FLASK_ENV=development poetry run flask run

lint:
	flake8 run.py blog

.PHONY: run, lint
