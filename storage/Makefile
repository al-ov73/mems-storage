start-minio-api:
		uvicorn app.main:app --reload --port 1234

start-minio:
		./minio server ./minio --address ":9000" --console-address ":9001"

docker-build:
		docker build . -t s3_storage:latest

docker-run:
		docker run -p 6789:8000 s3_storage