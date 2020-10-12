run_dev:
	FLASK_APP=run.py FLASK_ENV=development poetry run flask run $(ARGS)

run_prod:
	poetry run gunicorn -w 3 run:app

lint:
	flake8 run.py flask_blog

.PHONY: run_dev, run_prod, lint
