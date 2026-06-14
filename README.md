# URL Shortener — FastAPI + Redis + PostgreSQL

A URL shortener built with FastAPI. Supports Google OAuth 2.0 authentication, URL shortening with Redis cache-aside, click tracking, and hourly background sync via Celery.

## Tech Stack
- FastAPI + Uvicorn
- PostgreSQL + SQLAlchemy + Alembic
- Redis (URL cache + click counting + rate limiting)
- Celery + Celery Beat (background click sync)
- Pydantic v2
- python-jose (JWT)
- pytest (testing)
- Docker + Docker Compose

## Setup

### Option A — Local

1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Copy and fill environment variables
```bash
cp .env.example .env
```

3. Run migrations
```bash
alembic upgrade head
```

4. Start the server
```bash
uvicorn app.main:app --reload
```

5. Start Celery worker and beat (separate terminals)
```bash
celery -A app.celery_app worker --loglevel=info --pool=solo
celery -A app.celery_app beat --loglevel=info
```

### Option B — Docker

```bash
docker-compose up --build
```

Starts FastAPI, PostgreSQL, Redis, Celery worker, and Celery beat in one command.

## Endpoints

### Auth
| Method | Endpoint | Description | Protected |
|--------|----------|-------------|-----------|
| GET | /auth/google/login | Redirect to Google login | No |
| GET | /auth/google/callback | Google OAuth callback | No |
| POST | /auth/google/refresh | Rotate refresh token | No |
| POST | /auth/google/logout | Revoke tokens | Yes |
| GET | /users/me | Get current user | Yes |

### URL Shortener
| Method | Endpoint | Description | Protected |
|--------|----------|-------------|-----------|
| POST | /urls/ | Create shortened URL | Yes |
| GET | /urls/{short_code} | Redirect to original URL | No |
| GET | /urls/ | List all your URLs | Yes |
| DELETE | /urls/{short_code} | Deactivate a URL | Yes |
| GET | /urls/{short_code}/stats | URL click statistics | Yes |

## How It Works

**Authentication**
- Login with Google → receive access token (15 min) + refresh token (7 days)
- Access token is stateless JWT — verified on every protected request
- Refresh token stored in Redis — rotated on every /refresh call
- Logout blacklists the access token JTI in Redis until expiry

**URL Shortening**
- Submit a long URL → get a unique 6-character short code
- Every redirect checks Redis first — falls back to PostgreSQL on cache miss
- Cache is rebuilt on every miss with remaining TTL synced to link expiry
- All links expire after 7 days
- Private IPs and localhost URLs are blocked at creation

**Click Tracking**
- Every redirect increments a Redis counter atomically via INCR
- Celery Beat syncs click counts from Redis to PostgreSQL every hour
- Stats endpoint shows real-time count synced on demand

**Security**
- Rate limiting on redirect — 20 requests per IP per minute
- Private IP and localhost blocking (SSRF protection)
- JWT blacklisting on logout
- Ownership validation on delete and stats endpoints

## Future Improvements
- Custom short codes chosen by user
- Frontend dashboard for link management
- Analytics dashboard with click history over time
- Background Celery task already in place for periodic DB sync



