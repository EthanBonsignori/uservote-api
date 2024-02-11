from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from motor.core import AgnosticDatabase
import platform
import psutil

from app.database.database import get_database_client

router = APIRouter()


@router.get('/', include_in_schema=False)
@router.get('')
async def health(db: AgnosticDatabase = Depends(get_database_client)):
    try:
        # Check if the database is responsive
        await db.command('ping')
        db_status = 'up'
    except Exception:
        db_status = 'down'

    # Get system information
    system_info = {
        "system": platform.system(),
        "processor": platform.processor(),
        "architecture": platform.architecture(),
        "memory": psutil.virtual_memory()._asdict(),
        "disk": psutil.disk_usage('/')._asdict()
    }

    return JSONResponse(
        status_code=db_status == 'up' and 200 or 503,
        content={
            "database": db_status,
            "system_info": system_info
        }
    )
