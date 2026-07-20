# RailwayCrewSystem - TODO (Backend)

## Phase 2 (Database Finalization)
- [x] Fix/align Alembic heads and validate single head
- [x] Install psycopg dependency required for Alembic/DB connection
- [x] Ensure `alembic upgrade head` works with current DB migration state
- [ ] Add DB-level uniqueness + indexes for duty-instance design:
  - [ ] `assignments`: UNIQUE(shift_id, crew_id) and indexes on shift_id/crew_id/status
  - [ ] `availabilities`: UNIQUE(crew_id, available_date) and indexes on crew_id/available_date/status
- [ ] Create Alembic migration implementing the above constraints/indexes
- [ ] Update SQLAlchemy models accordingly
- [ ] Run `alembic upgrade head` to verify migrations apply
- [ ] Run `python -m compileall -q app` to verify code compiles

