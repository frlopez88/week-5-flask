# Social Media API — Documentation

A REST API built with Flask and PostgreSQL for a basic social media platform. Supports user management, posts, comments, and likes.

---

## Base URL

```
http://localhost:5000
```

---

## Health Check

### `GET /`

Confirms the server is running.

**Response `200`**
```json
{ "message": "Server Online" }
```

---

## Users `/users`

### `POST /users/` — Create a user

Registers a new user account.

**Request Body**
```json
{
  "user_name": "jdoe",
  "first_name": "John",
  "last_name": "Doe",
  "birt_date": "1995-06-15",
  "password": "secret123",
  "email": "jdoe@example.com"
}
```

| Field        | Type   | Required | Notes                  |
|--------------|--------|----------|------------------------|
| `user_name`  | string | ✅       | Primary key, unique    |
| `first_name` | string | ✅       |                        |
| `last_name`  | string | ✅       |                        |
| `birt_date`  | string | ✅       | Format: `YYYY-MM-DD`   |
| `password`   | string | ✅       | Max 20 characters      |
| `email`      | string | ✅       | Must be unique         |

**Response `201`**
```json
{ "message": "User Created" }
```

**Response `500`**
```json
{ "message": "error <details>" }
```

---

### `GET /users/<user_name>` — Get user by username

Returns public profile info for a user.

**URL Parameter**

| Parameter   | Type   | Description          |
|-------------|--------|----------------------|
| `user_name` | string | The user's username  |

**Response `200`**
```json
[
  {
    "user_name": "jdoe",
    "first_name": "John",
    "last_name": "Doe"
  }
]
```

**Response `500`**
```json
{ "message": "error <details>" }
```

---

### `POST /users/auth` — Authenticate a user

Validates a username and password combination.

**Request Body**
```json
{
  "user_name": "jdoe",
  "password": "secret123"
}
```

**Response `200`** — Credentials are valid
```json
{ "message": "User Auth" }
```

**Response `400`** — Invalid credentials
```json
{ "message": "Wrong Credentials" }
```

**Response `500`**
```json
{ "message": "error <details>" }
```

---

## Posts `/posts`

### `POST /posts/` — Create a post

Creates a new post for a user.

**Request Body**
```json
{
  "description": "Hello world!",
  "user_name": "jdoe"
}
```

| Field         | Type   | Required | Notes                          |
|---------------|--------|----------|--------------------------------|
| `description` | string | ✅       | Max 150 characters             |
| `user_name`   | string | ✅       | Must reference an existing user|

**Response `201`**
```json
{ "message": "Object Created" }
```

**Response `500`**
```json
{ "message": "error <details>" }
```

---

### `GET /posts/` — Get all posts

Returns all posts in the database.

**Response `200`**
```json
[
  {
    "post_id": 1,
    "description": "Hello world!",
    "user_name": "jdoe",
    "creation_date": "2026-05-07T10:30:00"
  }
]
```

**Response `500`**
```json
{ "message": "error <details>" }
```

---

## Comments `/comments`

### `POST /comments` — Add a comment

Adds a comment to a post.

**Request Body**
```json
{
  "user_name": "jdoe",
  "post_id": 1,
  "description": "Great post!"
}
```

| Field         | Type    | Required | Notes                           |
|---------------|---------|----------|---------------------------------|
| `user_name`   | string  | ✅       | Must reference an existing user |
| `post_id`     | integer | ✅       | Must reference an existing post |
| `description` | string  | ✅       | Max 100 characters              |

**Response `201`**
```json
{ "message": "Object Created" }
```

**Response `500`**
```json
{ "message": "error <details>" }
```

---

### `GET /comments/<post_id>` — Get comments for a post

Returns all comments on a specific post.

**URL Parameter**

| Parameter | Type    | Description |
|-----------|---------|-------------|
| `post_id` | integer | The post ID |

**Response `200`**
```json
[
  {
    "comment_id": 1,
    "user_name": "jdoe",
    "post_id": 1,
    "description": "Great post!"
  }
]
```

**Response `500`**
```json
{ "message": "error <details>" }
```

---

## Likes `/likes`

### `POST /likes/` — Like a post

Adds a like from a user to a post.

**Request Body**
```json
{
  "user_name": "jdoe",
  "post_id": 1
}
```

| Field       | Type    | Required | Notes                           |
|-------------|---------|----------|---------------------------------|
| `user_name` | string  | ✅       | Must reference an existing user |
| `post_id`   | integer | ✅       | Must reference an existing post |

**Response `201`**
```json
{ "message": "Object Created" }
```

**Response `500`**
```json
{ "message": "error <details>" }
```

---

### `GET /likes/<post_id>/countlikes` — Count likes on a post

Returns the total number of likes for a specific post.

**URL Parameter**

| Parameter | Type    | Description |
|-----------|---------|-------------|
| `post_id` | integer | The post ID |

**Response `200`**
```json
[
  { "likes": 42 }
]
```

**Response `500`**
```json
{ "message": "error <details>" }
```

---

## Database Schema

```
users
├── user_name     VARCHAR(50)  PK
├── first_name    VARCHAR(100)
├── last_name     VARCHAR(100)
├── birt_date     DATE
├── password      VARCHAR(20)
└── email         VARCHAR(50)  UNIQUE

posts
├── post_id        SERIAL       PK
├── description    VARCHAR(150)
├── user_name      VARCHAR(50)  FK → users.user_name
└── creation_date  TIMESTAMP    DEFAULT current_timestamp

comments
├── comment_id   SERIAL       PK
├── user_name    VARCHAR(50)  FK → users.user_name
├── post_id      INT          FK → posts.post_id
└── description  VARCHAR(100)

likes
├── like_id    SERIAL       PK
├── user_name  VARCHAR(50)  FK → users.user_name
└── post_id    INT          FK → posts.post_id
```

---

## Setup

### Prerequisites

- Python 3.x
- PostgreSQL

### Install dependencies

```bash
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_user
DB_PASS=your_password
DB_SSLMODE=require
```

### Run the server

```bash
python app.py
```

The server starts on `http://localhost:5000` with debug mode enabled. The database tables are created automatically on startup.

---

## Error Handling

All endpoints return a consistent error shape on failure:

```json
{ "message": "error <details>" }
```

HTTP status codes used:

| Code | Meaning            |
|------|--------------------|
| 200  | OK                 |
| 201  | Created            |
| 400  | Bad Request        |
| 500  | Internal Server Error |
