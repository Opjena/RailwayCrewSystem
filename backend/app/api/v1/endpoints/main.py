from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.main_data import MainDataResponse, CTOUpdate, ShedUpdate, LocoUpdate
from app.schemas.common import APIResponse, PaginatedResponse
from app.services.main_service import MainService
from app.auth.permissions import require_controller, require_supervisor

router = APIRouter(
    prefix="/main",
    tags=["Main Data / Dashboard"],
)


@router.get("")
def get_all_main(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    crew_id: str | None = Query(None, description="Filter by crew ID"),
    train_no: str | None = Query(None, description="Filter by train number"),
    station: str | None = Query(None, description="Filter by station (from/to)"),
    status: str | None = Query(None, description="Filter by status"),
    is_active: bool | None = Query(None, description="Filter by active status"),
    search: str | None = Query(None, description="Keyword search"),
    sort: str = Query("id", description="Sort column"),
    order: str = Query("asc", description="Sort order (asc/desc)"),
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Get all MainData records with pagination, filtering, and search"""
    service = MainService(db, request)
    result = service.get_all_main(
        skip=skip,
        limit=limit,
        crew_id=crew_id,
        train_no=train_no,
        station=station,
        status=status,
        is_active=is_active,
        search=search,
        sort=sort,
        order=order,
    )
    return APIResponse(
        success=True,
        message="MainData records retrieved successfully",
        data=PaginatedResponse(
            items=[
                MainDataResponse.model_validate(m).model_dump()
                for m in result["items"]
            ],
            total=result["total"],
            page=result["page"],
            page_size=result["page_size"],
            total_pages=result["total_pages"],
        ).model_dump(),
    )


@router.get("/active")
def get_active_crew(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Get all currently active (signed-on) crew"""
    service = MainService(db, request)
    result = service.get_active_crew(skip=skip, limit=limit)
    return APIResponse(
        success=True,
        message="Active crew retrieved successfully",
        data=PaginatedResponse(
            items=[
                MainDataResponse.model_validate(m).model_dump()
                for m in result["items"]
            ],
            total=result["total"],
            page=result["page"],
            page_size=result["page_size"],
            total_pages=result["total_pages"],
        ).model_dump(),
    )


@router.get("/train/{train_no}")
def get_by_train(
    train_no: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Get active crew assigned to a train"""
    service = MainService(db, request)
    result = service.get_by_train(train_no)
    return APIResponse(
        success=True,
        message="Active crew by train retrieved successfully",
        data=PaginatedResponse(
            items=[
                MainDataResponse.model_validate(m).model_dump()
                for m in result["items"]
            ],
            total=result["total"],
            page=result["page"],
            page_size=result["page_size"],
            total_pages=result["total_pages"],
        ).model_dump(),
    )


@router.get("/station/{station}")
def get_by_station(
    station: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Get active crew at a station"""
    service = MainService(db, request)
    result = service.get_by_station(station)
    return APIResponse(
        success=True,
        message="Active crew by station retrieved successfully",
        data=PaginatedResponse(
            items=[
                MainDataResponse.model_validate(m).model_dump()
                for m in result["items"]
            ],
            total=result["total"],
            page=result["page"],
            page_size=result["page_size"],
            total_pages=result["total_pages"],
        ).model_dump(),
    )


@router.get("/crew/{crew_id}")
def get_by_crew(
    crew_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Get active record for a specific crew"""
    service = MainService(db, request)
    main = service.get_by_crew(crew_id)
    return APIResponse(
        success=True,
        message="Active crew record retrieved successfully",
        data=MainDataResponse.model_validate(main).model_dump(),
    )


@router.put("/{main_id}/cto")
def update_cto(
    main_id: int,
    data: CTOUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    """Update CTO details for a MainData record (Admin, Controller)"""
    service = MainService(db, request)
    main = service.update_cto(main_id, data, actor_username=current_user.username)
    return APIResponse(
        success=True,
        message="CTO details updated successfully",
        data=MainDataResponse.model_validate(main).model_dump(),
    )


@router.put("/{main_id}/shed")
def update_shed(
    main_id: int,
    data: ShedUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    """Update Shed for a MainData record (Admin, Controller)"""
    service = MainService(db, request)
    main = service.update_shed(main_id, data, actor_username=current_user.username)
    return APIResponse(
        success=True,
        message="Shed updated successfully",
        data=MainDataResponse.model_validate(main).model_dump(),
    )


@router.put("/{main_id}/loco")
def update_loco(
    main_id: int,
    data: LocoUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    """Update Loco details for a MainData record (Admin, Controller)"""
    service = MainService(db, request)
    main = service.update_loco(main_id, data, actor_username=current_user.username)
    return APIResponse(
        success=True,
        message="Loco details updated successfully",
        data=MainDataResponse.model_validate(main).model_dump(),
    )

