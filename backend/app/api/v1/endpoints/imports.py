from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/import", tags=["Excel Import"])


@router.post("/excel")
def import_excel(file: UploadFile = File(...)):
    # TODO: implement parsing + persistence + import logs
    # Return a placeholder import response.
    return {
        "filename": file.filename,
        "status": "not_implemented_yet",
    }

