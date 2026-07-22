from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.main_data import MainDataResponse, CTOUpdate, ShedUpdate, LocoUpdate
from app.schemas.common import APIResponse
from app.services.main_service import MainDataService
from app.auth.permissions import require_admin, require_supervisor

router = APIRouter(
    prefix="/main-data",
    tags=["Main Data"],
)


@router.post(
    "/from-signon/{signon_id}",
    response_model=APIResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create MainData from SignOn",
    description="Creates a MainData record from an existing SignOn record. Requires admin role.",
)
def create_from_signon(
    signon_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Create MainData from SignOn (Admin only)"""
    service = MainDataService(db, request)
    main_data = service.create_from_signon(signon_id, actor_username=current_user.username)
    return APIResponse(
        success=True,
        message="MainData record created successfully",
        data=MainDataResponse.model_validate(main_data).model_dump(),
    )


@router.get(
    "",
    response_model=APIResponse,
    summary="Get all MainData records",
    description="Retrieve all MainData records with pagination.",
)
def get_all_main_data(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Get all MainData records"""
    service = MainDataService(db, request)
    records = service.get_all_main_data(skip=skip, limit=limit)
    return APIResponse(
        success=True,
        message="MainData records retrieved successfully",
        data=[MainDataResponse.model_validate(r).model_dump() for r in records],
    )


@router.get(
    "/{main_id}",
    response_model=APIResponse,
    summary="Get a MainData record by ID",
    description="Retrieve a specific MainData record by its ID.",
)
def get_main_data(
    main_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Get a specific MainData record by ID"""
    service = MainDataService(db, request)
    main_data = service.get_by_id_or_404(main_id)
    return APIResponse(
        success=True,
        message="MainData record retrieved successfully",
        data=MainDataResponse.model_validate(main_data).model_dump(),
    )


@router.put(
    "/{main_id}/cto",
    response_model=APIResponse,
    summary="Update CTO details",
    description="Update CTO train number, station, and time. Requires admin role.",
)
def update_cto(
    main_id: int,
    data: CTOUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Update CTO details (Admin only)"""
    service = MainDataService(db, request)
    main_data = service.update_cto(main_id, data, actor_username=current_user.username)
    return APIResponse(
        success=True,
        message="CTO details updated successfully",
        data=MainDataResponse.model_validate(main_data).model_dump(),
    )


@router.put(
    "/{main_id}/shed",
    response_model=APIResponse,
    summary="Update shed details",
    description="Update shed information. Requires admin role.",
)
def update_shed(
    main_id: int,
    data: ShedUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Update shed details (Admin only)"""
    service = MainDataService(db, request)
    main_data = service.update_shed(main_id, data, actor_username=current_user.username)
    return APIResponse(
        success=True,
        message="Shed details updated successfully",
        data=MainDataResponse.model_validate(main_data).model_dump(),
    )


@router.put(
    "/{main_id}/loco",
    response_model=APIResponse,
    summary="Update locomotive details",
    description="Update locomotive numbers (loco1, loco2, loco3). Requires admin role.",
)
def update_loco(
    main_id: int,
    data: LocoUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Update locomotive details (Admin only)"""
    service = MainDataService(db, request)
    main_data = service.update_loco(main_id, data, actor_username=current_user.username)
    return APIResponse(
        success=True,
        message="Locomotive details updated successfully",
        data=MainDataResponse.model_validate(main_data).model_dump(),
    )
