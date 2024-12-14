start:
		poetry run fastapi run app/main.py

test:
		pytest

coverage:
		pytest --cov

lint:
		poetry run flake8 ./app

migration:
		alembic revision --autogenerate -m "$(n)"

migrate:
		alembic upgrade head

parse:
		poetry run python3 parse.py