start-api:
		uvicorn api.app.main:app --reload

start-minio-api:
		uvicorn storage.main:app --reload --port 1234

start-minio:
		./minio server ./storage/minio --address ":9000" --console-address ":9001"

test:
		pytest

docker-build:
		docker compose -f docker-compose.yml build

docker-run:
		docker compose -f docker-compose.yml up

docker:
		docker compose run -P api bash

connect-frontend:
		docker exec -it mems-frontend /bin/sh
		