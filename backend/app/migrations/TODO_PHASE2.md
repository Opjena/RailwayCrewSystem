# Phase 2 - TODO

## Database finalization
- [ ] Add unique constraint for `assignments(shift_id, crew_id)`
- [ ] Add indexes for `assignments`: shift_id, crew_id, status
- [ ] Add unique constraint for `availabilities(crew_id, available_date)`
- [ ] Add indexes for `availabilities`: crew_id, available_date, status
- [ ] Create Alembic migration implementing the above
- [ ] Run `alembic upgrade head`
- [ ] Compile check: `python -m compileall -q app`

