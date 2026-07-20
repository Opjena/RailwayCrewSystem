# Railway Crew Management System - Backend Setup Guide

## Prerequisites
- Docker & Docker Compose installed
- Python 3.11+ (for local development)
- PostgreSQL 15+ (if running locally without Docker)

## Quick Start with Docker

### 1. Start Services
```bash
docker-compose up -d
```

This will:
- Start PostgreSQL database
- Build and run FastAPI backend
- Run migrations automatically

### 2. Access the API
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Database**: localhost:5432

### 3. Stop Services
```bash
docker-compose down
```

---

## Local Development (Without Docker)

### 1. Setup Environment
```bash
cd backend
cp .env.example .env
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database
```bash
# Create database
psql -U postgres -c "CREATE DATABASE railway_crew_system;"

# Run migrations
alembic upgrade head
```

### 5. Run Server
```bash
uvicorn app.main:app --reload
```

---

## Database Migrations

### Create New Migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback Last Migration
```bash
alembic downgrade -1
```

---

## API Documentation

### Authentication
- **Endpoint**: `POST /api/v1/auth/login`
- **Body**: `{"username": "admin", "password": "password"}`
- **Response**: JWT token

### Create Crew Member
- **Endpoint**: `POST /api/v1/crew`
- **Headers**: `Authorization: Bearer {token}`
- **Body**:
```json
{
  "crew_id": "CR001",
  "full_name": "John Doe",
  "department": "Driver",
  "email": "john@example.com",
  "phone": "+1234567890"
}
```

### Create Shift
- **Endpoint**: `POST /api/v1/schedule/shifts`
- **Headers**: `Authorization: Bearer {token}`
- **Body**:
```json
{
  "shift_date": "2026-07-25",
  "shift_type": "Morning",
  "start_time": "06:00:00",
  "end_time": "14:00:00",
  "crew_required": 3,
  "location": "Central Station"
}
```

### Assign Crew to Shift
- **Endpoint**: `POST /api/v1/schedule/assignments`
- **Headers**: `Authorization: Bearer {token}`
- **Body**:
```json
{
  "shift_id": 1,
  "crew_id": 1,
  "status": "Assigned"
}
```

---

## User Roles & Permissions

| Role | Permissions |
|------|-------------|
| Admin | Full access to all resources |
| Controller | Create/manage shifts and assignments |
| Supervisor | Manage crew availability |
| LobbyOperator | View-only access to schedule |
| Viewer | Read-only access |

---

## Testing

```bash
pytest backend/tests/ -v
```

---

## Troubleshooting

### Database Connection Error
```bash
# Check if PostgreSQL is running
docker ps

# View logs
docker-compose logs db
```

### Port Already in Use
```bash
# Change port in docker-compose.yml
# Or kill existing process
lsof -i :8000  # Find process
kill -9 <PID>  # Kill process
```

### Migration Errors
```bash
# Reset database (warning: clears all data)
alembic downgrade base
alembic upgrade head
```

---

## Project Structure

```
backend/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/
│   │   │   ├── auth.py
│   │   │   ├── crew.py
│   │   │   ├── schedule.py
│   │   │   ├── dashboard.py
│   │   │   ├── reports.py
│   │   │   └── setting.py
│   │   └── api.py
│   ├── models/
│   │   ├── user.py
│   │   ├── crew.py
│   │   ├── shift.py
│   │   ├── assignment.py
│   │   └── availability.py
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── core/
│   ├── auth/
│   ├── db/
│   └── main.py
├── alembic/
│   └── versions/
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```
