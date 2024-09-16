start:
		gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --reload
		# alembic upgrade head && gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --reload

test:
		pytest


makemigrations:
		alembic revision --autogenerate -m "add labels m2m back populates"

migrate:
		alembic upgrade head