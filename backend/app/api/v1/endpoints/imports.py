from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from app.auth.permissions import require_controller, require_authenticated
from app.db.database import get_db
from app.models.import_log import ImportLog
from app.schemas.import_log import ImportLogResponse
from app.services.audit_log_service import AuditLogService

router = APIRouter(prefix="/import", tags=["Excel Import"])


@router.post("/excel")
async def import_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Only Excel files are allowed")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    log = ImportLog(filename=file.filename, status="processing")
    db.add(log)
    db.commit()
    db.refresh(log)

    log.status = "completed"
    db.commit()
    db.refresh(log)

    AuditLogService.log_action(
        db,
        actor_username=current_user.username,
        action="create",
        entity="import_log",
        entity_id=str(log.id),
    )

    return {
        "import_log_id": log.id,
        "filename": log.filename,
        "status": log.status,
        "bytes_processed": len(content),
    }


@router.get("/logs", response_model=list[ImportLogResponse])
def list_import_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    return (
        db.query(ImportLog)
        .order_by(ImportLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
