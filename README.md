# 📊 Cost Management API

A simple API for managing costs with CRUD operations (Create, Read, Update, Delete), user authentication, and user-specific cost management.

---

## 📖 Project Description

This is a practice project for learning FastAPI, Pydantic, SQLAlchemy (ORM), Alembic (migrations), authentication, JWT tokens, and cookie-based authentication.

Data is stored persistently in an SQLite database.

Users can register and log in to the application. After a successful login, an access token and a refresh token are stored in HTTP cookies. The access token is required to access protected endpoints such as the current user information and cost management endpoints.

Each cost belongs to a specific user, and users can only access and manage their own costs.

---

## 🛠️ Technologies Used

* **Python 3.11+**
* **FastAPI** (for building the API)
* **Pydantic V2** (for data validation)
* **SQLAlchemy** (ORM for database interaction)
* **Alembic** (for database migrations)
* **JWT** (for authentication tokens)
* **HTTP Cookies** (for storing access and refresh tokens)
* **Uvicorn** (for running the server)

---

## 🚀 Installation & Running

### 1. Clone the repository

```bash
git clone https://github.com/your-username/cost-management-api.git
cd cost-management-api
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Run the application

```bash
uvicorn main:app --reload
```

After running, the API will be available at:

➡️ http://127.0.0.1:8000

Swagger UI documentation:

➡️ http://127.0.0.1:8000/docs

---

📋 Available Endpoints

### Authentication

| Method | Path             | Description                                      |
| ------ | ---------------- | ------------------------------------------------ |
| POST   | `/auth/register` | Register a new user                              |
| POST   | `/auth/login`    | Login and receive access and refresh tokens      |
| POST   | `/auth/refresh`  | Refresh the access token using the refresh token |

### User

| Method | Path       | Description                          |
| ------ | ---------- | ------------------------------------ |
| GET    | `/user/me` | Get the currently authenticated user |

### Costs

| Method | Path          | Description                         |
| ------ | ------------- | ----------------------------------- |
| POST   | `/costs/`     | Create a new cost                   |
| GET    | `/costs/`     | Get costs of the authenticated user |
| GET    | `/costs/{id}` | Get a cost by ID                    |
| PUT    | `/costs/{id}` | Update a cost                       |
| DELETE | `/costs/{id}` | Delete a cost                       |

### Costs Pagination

The `GET /costs/` endpoint supports pagination using `limit` and `skip` query parameters.

* `limit`: Number of costs to return. Minimum: `1`, Maximum: `50`, Default: `10`
* `skip`: Number of costs to skip. Default: `0`

Example:

```text
GET /costs/?limit=10&skip=0
```

---

## 🔐 Authentication

Authentication is based on JWT access and refresh tokens.

After a successful login:

* `access_token` is stored in an HTTP cookie.
* `refresh_token` is stored in an HTTP cookie.
* Protected endpoints require a valid access token.
* The refresh endpoint requires a valid refresh token.
* Access and refresh token types are validated separately.

Protected endpoints include:

* `/user/me`
* `/costs/`
* `/costs/{id}`

---

## 👤 Users

Each user has the following information:

* `id`
* `username`
* `email`
* `hashed_password`
* `is_active`

The password is stored as a hash and is not returned through the API.

---

## 💰 Costs

Each cost contains:

* `id`
* `description`
* `amount`
* `user_id`

Each cost belongs to one user through the `user_id` foreign key.

Users can only access, update, and delete their own costs.

The current cost description supports up to **100 characters**, and the amount must be greater than `0`.

---

## 🗄️ Database Relationship

The relationship between users and costs is:

```text
User
 |
 | 1
 |
 | *
 ↓
Cost
```

One user can have multiple costs, while each cost belongs to one user.

---

## 🔄 Authentication Flow

```text
Register
   ↓
Login
   ↓
Access Token + Refresh Token
   ↓
HTTP Cookies
   ↓
Access protected endpoints
```

When the access token needs to be refreshed:

```text
Refresh Token
      ↓
POST /auth/refresh
      ↓
New Access Token
```
