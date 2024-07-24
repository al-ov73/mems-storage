start-api:
		uvicorn api.app.main:app --reload

start-minio-api:
		uvicorn storage.main:app --reload --port 1234

start-minio:
		./minio server ./storage/minio --address ":9000" --console-address ":9001"

test:
		pytest

# alembic revision --autogenerate -m "rm url field"
# alembic upgrade head