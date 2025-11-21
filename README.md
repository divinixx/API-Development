# FastAPI Application

A production-ready FastAPI application with PostgreSQL database, JWT authentication, and user/post management.

## Features

- ✅ User registration and authentication
- ✅ JWT token-based authorization
- ✅ Post creation, reading, updating, and deletion
- ✅ Vote system for posts
- ✅ PostgreSQL database with Alembic migrations
- ✅ CORS middleware enabled
- ✅ Password hashing with bcrypt

## Local Development

### Prerequisites

- Python 3.9+
- PostgreSQL database

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

5. Update `.env` with your database credentials and secret key

6. Run database migrations:
   ```bash
   alembic upgrade head
   ```

7. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## Deployment to Render

### Environment Variables

Set the following environment variables in your Render dashboard:

- `DATABASE_HOSTNAME` - Your PostgreSQL host
- `DATABASE_PORT` - Database port (usually 5432)
- `DATABASE_PASSWORD` - Database password
- `DATABASE_NAME` - Database name
- `DATABASE_USERNAME` - Database username
- `SECRET_KEY` - A strong random string for JWT (generate with: `openssl rand -hex 32`)
- `ALGORITHM` - HS256
- `ACCESS_TOKEN_EXPIRE_MINUTES` - 30

### Steps

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `uvicorn app.main:app --host=0.0.0.0 --port=8000`
5. Add environment variables
6. Create a PostgreSQL database in Render and link it
7. Deploy!

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app and routes
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic schemas
│   ├── database.py       # Database connection
│   ├── config.py         # Configuration settings
│   ├── oauth2.py         # JWT authentication
│   ├── utils.py          # Password hashing utilities
│   └── routers/          # API route modules
│       ├── auth.py
│       ├── post.py
│       ├── user.py
│       └── vote.py
├── alembic/              # Database migrations
├── requirements.txt      # Python dependencies
├── Procfile             # Render deployment config
└── .env.example         # Environment variables template
```

## License

MIT
