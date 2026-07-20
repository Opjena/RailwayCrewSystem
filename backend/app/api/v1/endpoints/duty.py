from fastapi import APIRouter

router = APIRouter(prefix="/duty", tags=["Duty"])


@router.get("")
def list_duties():
    # TODO: implement once Duty model/repository are added
    return []

