# 🍽️ Restaurant Reservation API

A production-ready RESTful API for managing restaurant reservations, built with Django REST Framework.

![Django](https://img.shields.io/badge/Django-4.2-green)
![DRF](https://img.shields.io/badge/DRF-3.14-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-ready-blue)

## Features

- JWT Authentication (register, login, logout)
- Role-based access control (Customer, Owner, Admin)
- Restaurant & table management
- Reservation conflict detection
- Filtering, searching, pagination
- Swagger / OpenAPI documentation
- Dockerized with PostgreSQL

## Tech Stack

| Technology | Version |
|---|---|
| Python | 3.11 |
| Django | 4.2 |
| Django REST Framework | 3.14 |
| PostgreSQL | 15 |
| Docker & Docker Compose | latest |
| JWT | SimpleJWT |

## Quick Start (Docker)

```bash
git clone https://github.com/orifrustamovich/restaurant-reservation-api
cd restaurant-reservation-api

cp .env.example .env    # configure file .env 

docker compose up --build
```

API: http://localhost:8000/api/  
Docs: http://localhost:8000/api/docs/  
Admin: http://localhost:8000/admin/

## Quick Start (Local)

```bash
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# configure file .env  (DB_HOST=localhost)
cp .env.example .env

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Environment Variables

`.env.example` view file:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=restaurant_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=db
DB_PORT=5432
```
## Setup

```bash
cp .env.example .env
# Fill the .env file with your own values
docker compose up --build
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login & get JWT tokens |
| POST | `/api/auth/logout/` | Logout (blacklist token) |
| GET/PUT | `/api/auth/profile/` | View & update profile |

### Restaurants

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| GET | `/api/restaurants/` | List all restaurants | Any |
| POST | `/api/restaurants/` | Create restaurant | Owner |
| GET | `/api/restaurants/{id}/` | Restaurant detail | Any |
| PUT | `/api/restaurants/{id}/` | Update restaurant | Owner |
| DELETE | `/api/restaurants/{id}/` | Delete restaurant | Owner |
| GET | `/api/restaurants/{id}/tables/` | List tables | Any |
| GET | `/api/restaurants/my-restaurants/` | My restaurants | Owner |

### Tables

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| GET | `/api/tables/` | List tables | Any |
| POST | `/api/tables/` | Create table | Owner |
| PUT | `/api/tables/{id}/` | Update table | Owner |
| DELETE | `/api/tables/{id}/` | Delete table | Owner |

### Reservations

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| GET | `/api/reservations/` | My reservations | Auth |
| POST | `/api/reservations/` | Create reservation | Customer |
| GET | `/api/reservations/{id}/` | Reservation detail | Auth |
| POST | `/api/reservations/{id}/cancel/` | Cancel reservation | Customer |
| POST | `/api/reservations/{id}/confirm/` | Confirm reservation | Owner |

## Filtering & Search

```bash
# Search Restaurant
GET /api/restaurants/?search=sushi&min_rating=4.0&is_active=true

```

## 👨‍💻 Author

**Orifjon Toshtemirov**  
🔗 GitHub: https://github.com/orifrustamovich  
📧 Email: oriffrustamovich@gmail.com
