from fastapi import APIRouter

router = APIRouter(prefix="/train", tags=["Train"])


@router.get("")
def list_trains():
    # TODO: implement once Train model/repository are added
    return []

