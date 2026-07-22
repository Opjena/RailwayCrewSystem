# Railway Crew Management System - Implementation Progress

## Bug Fixes
- [ ] Fix: JSON-serialize old_value/new_value in base_service.py AuditLog (dict can't bind to Text column in SQLite)
- [ ] Fix: Remove duplicate router prefixes from api.py for cms, signon, main, archive (causes 404)
- [ ] Fix: Change GET crew endpoints from require_supervisor to require_authenticated (viewer test fails)

