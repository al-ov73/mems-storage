[![Code checks](https://github.com/al-ov73/mems-storage/actions/workflows/tests.yml/badge.svg)](https://github.com/al-ov73/mems-storage/actions/workflows/tests.yml)
[![Api Linter](https://github.com/al-ov73/mems-storage/actions/workflows/python_linter.yml/badge.svg)](https://github.com/al-ov73/mems-storage/actions/workflows/python_linter.yml)
https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/al-ov73/2c5b53a767ccc15e5e119d945406e200/raw/covbadge.json

<br/>
![eslint](https://img.shields.io/badge/eslint-3A33D1?style=for-the-badge&logo=eslint&logoColor=white)

Memes storage
---
Microservices based service for storage your favorite memes.</br>
![Untitled (1)](https://github.com/user-attachments/assets/f6e1e9f9-c463-4093-a185-fb6e969e20e6)

---
**Services**:</br>
1. React service:</br>
React frontend app with CRUD functionality. Used Redux/Redux Toolkit service.</br>
[Documentation](https://github.com/al-ov73/mems-storage/blob/main/frontend/README.md)</br>
2. Api service:</br>
FastAPI web-service with JWT-based authorization and Bearer token-transport. Requests to Postgres database and other services cached by Redis. Covered by Pytest.</br>
Store memes data in postgres DB.</br>
Store image files in S3 storage (other michroservice).</br>
[Documentation](https://github.com/al-ov73/mems-storage/blob/main/api/README.md)</br>
3. Minio storage service:</br>
Fast-API web service to store images. Used Minio app to connect to S3-storage.</br>
[Documentation](https://github.com/al-ov73/mems-storage/blob/main/storage/README.md)</br>
---
**To start localy**:
1. Clone repository
```commandline
git clone git@github.com:al-ov73/mems-storage.git && cd mems-storage
```
2. fill .env-non-dev (or rename .env-non-dev_example to use default values)
3. build and run docker containers
```
make docker-build
make docker
```
4. Start api application
```
make start
```
Also you can run tests:
```
make test
```

TODO:</br>
- бейджик Pytest
- смоделировать все ошибки и обработать их
- убрать bd.commit из роутеров
- аватарка + кабинет
- админка