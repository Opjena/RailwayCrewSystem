from fastapi import APIRouter

router = APIRouter(prefix="/audit", tags=["Audit Logs"])


@router.get("")
def list_audit_logs():
    # TODO: implement once AuditLog model/repository are added
    return []

