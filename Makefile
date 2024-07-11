start:
		uvicorn api.main:app --reload

minio:
        minio server ~/minio --console-address :9001
