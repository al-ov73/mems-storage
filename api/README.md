***Api memes***

Api для взаимодействия с мемами, сообщениями в чате, комментариями и лайками.</br>

Схема связей моделей БД ([drawSQL](https://drawsql.app/teams/myteam-1122/diagrams/mems-storage)):</br>
![drawSQL-image-export-2024-09-01](https://github.com/user-attachments/assets/73c4b7f8-107e-432a-96d6-4c23a6013108)

***Install***
```
poetry install
poetry shell
uvicorn app.main:app --reload
```

***Api documentation***</br>

GET "/memes"</br>

```
[
  {
    "id": 1,
    "name": "first meme",
    "created_at": "2024-07-10T10:11:43.827198Z"
  },
  {
    "id": 2,
    "name": "second meme",
    "created_at": "2024-07-10T10:13:58.223369Z"
  },
]
```
GET "/memes/{meme_id}"</br>

```
{
        "meme": {
            "id": 1,
            "name": "first meme",
            "created_at": "2024-07-10T10:11:43.827198Z"
          },
        "link": link_to_meme,
    }

```

POST "/memes"</br></br>
*Request body:</br>
file: string($binary)</br>
filename: string*
```
{
  "id": 1,
  "name": "first meme",
  "created_at": "2024-07-10T10:11:43.827198Z",
  "is_uploaded": True,
}
```

DELETE "/memes/{meme_id}"</br>

```
{
  "id": 1,
  "name": "first meme",
  "created_at": "2024-07-10T10:11:43.827198Z"
},
```


PUT "/memes/{meme_id}"</br></br>
*Request body:</br>
file: string($binary)</br>
filename: string*
```
{
  "id": 1,
  "name": "new name",
  "created_at": "2024-07-10T10:11:43.827198Z",
}
```
