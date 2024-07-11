Memes storage
---
<b>Api interface</b></br>

GET "/"</br>
Response:
```
[
  {
    "id": "2fee8429-cde0-4312-b87c-e8e67359001d",
    "name": "first meme",
    "url": "google.com",
    "created_at": "2024-07-10T10:11:43.827198Z"
  },
  {
    "id": "8368dcef-d9f0-4737-89cf-8a9ceb9591ee",
    "name": "second meme",
    "url": "yandex.com",
    "created_at": "2024-07-10T10:13:58.223369Z"
  },
]
```


install-minio:
    wget https://dl.min.io/server/minio/release/linux-amd64/archive/minio_20240704142545.0.0_amd64.deb -O minio.deb
    sudo dpkg -i minio.deb

minio default credentials:
    minioadmin
