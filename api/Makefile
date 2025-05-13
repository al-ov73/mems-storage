start:
		poetry run fastapi run app/main.py --reload

test:
		pytest

coverage:
		pytest --cov

lint:
		poetry run flake8 ./app

migration:
		poetry run alembic revision --autogenerate -m "$(n)"

migrate:
		poetry run alembic upgrade head

parse:
		poetry run python3 parse.py

black:
		poetry run black -l 120 .

isort:
		poetry run isort .

format: isort black