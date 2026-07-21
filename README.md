# Railway Crew Management System (RCMS)

A modern Railway Crew Management System built with:

- FastAPI
- React + TypeScript
- PostgreSQL
- SQLAlchemy
- Playwright
- WhatsApp Integration

## Project Structure

- `backend/` - FastAPI + PostgreSQL backend (deployable MVP)

## Deployable MVP (Backend-first)

### Included modules
- Authentication
- User Management
- Crew Management
- Schedule (Shift / Assignment / Availability)
- Dashboard APIs
- Reports APIs
- Lobby APIs
- Train APIs
- Duty APIs
- Excel Import APIs (with import logs)
- Audit Log APIs

### Quick start

```bash
docker-compose up --build
```

API will be available at:
- `http://localhost:8000`
- `http://localhost:8000/docs`

For detailed local setup and smoke checks, see:
- `/home/runner/work/RailwayCrewSystem/RailwayCrewSystem/backend/SETUP.md`
