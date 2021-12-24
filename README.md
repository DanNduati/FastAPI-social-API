<h1 align="center">
    FastAPI Social API
</h1>

### This is restful CRUD social API built with FastAPI framework 
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Authentication**: [Oauth2](https://fastapi.tiangolo.com/tutorial/security/)
- **Deployment**: [Heroku](https://www.heroku.com/)
- **Containerization**: [Docker](https://www.docker.com/)

## Prerequisites
[Python](https://www.python.org/downloads/)

## Installation
Clone the repository
```bash
git clone git@github.com:DanNduati/FastAPI-social-API.git
```
Create a python virtual environment activate it
```bash
python3 -m venv env
```
```bash
source venv/bin/activate
```
Create a `.env` file similar to [`.env.example`](https://github.com/DanNduati/FastAPI-social-API/blob/main/.env.example).

Install dependencies
```bash
pip install -r requirements.txt
```
Run the server with:
```bash
uvicorn app.main:app --reload
```

## API Endpoints Overview
### 1. Auth Endpoint
OAuth2 authentication implementation, with password hashing and JWT tokens.

```http
POST /login
```

__Sample response__
```json
{
  "access_token": "string",
  "token_type": "string"
}
```

### 2. Users Endpoints
create/register a user
```http
POST /users/
```

__Sample response__
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2021-12-24T10:53:04.455Z"
}
```
Get user by id
```http
GET /users/{user_id}
```

__Sample response__
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2021-12-24T10:53:04.455Z"
}
```
### 3. Posts Endpoint
Get all posts
```http
GET /posts/
```

__Sample response__
```json
[
  {
    "Post": {
      "title": "string",
      "content": "string",
      "published": true,
      "id": 0,
      "created_at": "2021-12-24T10:56:01.321Z",
      "user_id": 0,
      "owner": {
        "id": 0,
        "email": "user@example.com"
      }
    },
    "votes": 0
  }
]
```
Create a post
```http
POST /login
```
__Sample request body__
```json
{
  "title": "string",
  "content": "string",
  "published": true
}
```
__Sample response__
```json
{
  "title": "string",
  "content": "string",
  "published": true,
  "id": 0,
  "created_at": "2021-12-24T10:56:51.205Z",
  "user_id": 0,
  "owner": {
    "id": 0,
    "email": "user@example.com"
  }
}
```
Get latest post
```http
GET /posts/latest
```

__Sample response__
```json
{
  "Post": {
    "title": "string",
    "content": "string",
    "published": true,
    "id": 0,
    "created_at": "2021-12-24T11:02:11.832Z",
    "user_id": 0,
    "owner": {
      "id": 0,
      "email": "user@example.com"
    }
  },
  "votes": 0
}
```
Get a post by its id
```http
GET /posts/{post_id}
```

__Sample response__
```json
{
  "Post": {
    "title": "string",
    "content": "string",
    "published": true,
    "id": 0,
    "created_at": "2021-12-24T11:03:10.442Z",
    "user_id": 0,
    "owner": {
      "id": 0,
      "email": "user@example.com"
    }
  },
  "votes": 0
}
```
Update a post
```http
PUT /posts/{post_id}
```
__Sample request body__
```json
{
  "title": "string",
  "content": "string",
  "published": true
}
```
__Sample response__
```json
{
  "title": "string",
  "content": "string",
  "published": true,
  "id": 0,
  "created_at": "2021-12-24T11:03:52.891Z",
  "user_id": 0,
  "owner": {
    "id": 0,
    "email": "user@example.com"
  }
}
```
Delete a post
```http
DELETE /posts/{post_id}
```

### 4. Vote Endpoint
UpVote/Downvote a post
```http
POST /vote/
```
__Sample request body__
```json
{
  "post_id": 0,
  "direction": 1
}
```
## Getting Started with Fast API and Docker
[My Article](https://dev.to/danchei99/getting-started-with-fast-api-and-docker-part-1-54oo)

## Acknowledgment
Special thanks to [@Sanjeev-Thiyagarajan](https://github.com/Sanjeev-Thiyagarajan) for his excellent and very thorough [fastapi-youtube-tutorial-series](https://www.youtube.com/playlist?list=PL8VzFQ8k4U1IiGUWdBI7s9Y7dm-4tgCXJ)