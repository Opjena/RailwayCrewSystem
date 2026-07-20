from fastapi import APIRouter

router = APIRouter(prefix="/lobby", tags=["Lobby"])


@router.get("")
def list_lobbies():
    # TODO: implement once Lobby model/repository are added
    return []

