start-api:
		uvicorn api.main:app --reload

start-minio-api:
		uvicorn storage.main:app --reload --port 1234

start-minio:
		./minio server ./storage/minio --address ":9000" --console-address ":9001"

# alembic revision --autogenerate -m "Added required tables"
# alembic upgrade head