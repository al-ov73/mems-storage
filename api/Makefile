start:
# 		gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --reload
		alembic upgrade head && gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --reload

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