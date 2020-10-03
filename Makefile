run:
	FLASK_APP=run.py FLASK_ENV=development poetry run flask run

lint:
	flake8 run.py flask_blog

.PHONY: run, lint
