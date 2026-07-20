# RCMS Backend Completion Plan (PRD-aligned)

Goal: Complete missing PRD modules **without changing existing files**.

## Scope (PRD roadmap items)
1. Finalize Database Schema
   - Add migrations + models for: Lobby, Train, Duty, Import Logs, Audit Logs
2. Lobby Module
   - Models: Lobby
   - APIs: Lobby CRUD + list/filter
3. Train Module
   - Models: Train
   - APIs: Train CRUD + list/filter
4. Duty Module
   - Models: Duty, duty history links to crew/shift
   - APIs: Duty CRUD; duty history queries
5. Excel Import
   - API endpoint to upload file + async import worker
   - Import logs persisted
6. Dashboard
   - Ensure dashboards incorporate duty history metrics (extend via new endpoints if needed)
7. Reports
   - Add duty-based and import-based reports if required
8. Audit Logs
   - Capture create/update/delete events for major entities
   - Persist audit logs
9. CMS Automation
   - Provide hooks / scheduled job entry points (initial stub)
10. Frontend
   - Out of backend scope

## Constraints
- Do **not** modify existing files.
- Only add new files (models, routers, schemas, services, repositories, migrations).

## Implementation strategy
- Create new module folders under `backend/app/`:
  - `app/models/lobby.py`, `app/models/train.py`, `app/models/duty.py`, `app/models/import_log.py`, `app/models/audit_log.py`
  - `app/schemas/*` equivalents
  - `app/repositories/*` equivalents
  - `app/services/*` equivalents
  - `app/api/v1/endpoints/lobby.py`, `train.py`, `duty.py`, `import.py`, `audit.py`
- Create integration via new route registration approach:
  - If existing `api.py` is immutable per constraint, add a new router aggregator file and ensure FastAPI includes it via an existing import path.
  - If that is impossible without editing, provide an alternative: document endpoints and expose via a separate ASGI app entry (new file `app/main_ext.py`) that can be run locally.

## Immediate blockers discovered
- Requirements install fails due to `psycopg[binary]==3.17.0` not available in this environment.
- This plan still creates code, but runtime tests may require adjusting dependency pins in `requirements.txt` (not allowed under your constraint).

## Deliverables I can add next (no changes to existing files)
- New PRD-aligned models/schemas/services/repos
- New endpoints for Lobby/Train/Duty/Import/Audit
- Alembic migration stub files (may require referencing current base metadata)
- A runnable alternative app entrypoint `app/main_ext.py` that wires the new routers (if existing wiring cannot be changed)

