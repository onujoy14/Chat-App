# Chat App API

A REST API built with FastAPI and PostgreSQL. Includes user registration, login with JWT authentication, and full CRUD operations.

## Tech stack
- FastAPI, SQLAlchemy, PostgreSQL, bcrypt, JWT

## How to run

```bash
git clone https://github.com/onujoy14/Chat-App.git
cd Chat-App
pip install -r requirement.txt
uvicorn main:app --reload
```

API runs at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

## Endpoints

- `POST /users` — Register a new user
- `POST /login` — Login and get a JWT token
- `GET /me` — Get your profile (protected)
- `GET /users` — Get all users
- `PUT /users/{id}` — Update a user
- `DELETE /users/{id}` — Delete a user

## Author
Onu Joy Ojima · [onujoy14@gmail.com](mailto:onujoy14@gmail.com)
