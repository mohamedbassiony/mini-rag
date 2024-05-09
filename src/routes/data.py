from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
import os
from helpers.config import get_settings, Settings
from controllers.DataController import DataController
from controllers import DataController, ProjectController
import aiofiles
from models import ResponseSignal
import logging
logger  = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    


    # validate the file properties
    is_valid, result_signal = DataController().validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_coda = status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result_signal
            }
        )
    
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path = data_controller.generate_unique_filename(
        orig_file_name=file.filename
        project_id = project_id
    )
    # file_path = os.path.join(
    #     project_dir_path,
    #     file.filename
    # )
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        
        logger.error(f"Error while uploading file{e}")
        return JSONResponse(

            status_coda = status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_UPLOAD_FAILED.VALEU
            }
        )
    

    return JSONResponse(
        status_coda = status.HTTP_400_BAD_REQUEST,
        content={
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value
        }
    )


# def validate_uploaded_file(file: UploadFile):
#     FILE_ALLOWED_TYPES=["text/plain", "application/pdf"]
#     FILE_MAX_SIZE=10
#     size_scale = 1048576 # convert MB to bytes


#     if file.content_type not in FILE_ALLOWED_TYPES:
#         return False, "file_type_not_supported"
    
#     if file.size > FILE_MAX_SIZE * size_scale:
#         return False, "file_size_exceeded"
    
#     return True, "success"

# @data_router.post("/upload/{project_id}")
# async def upload_data(project_id: str, file: UploadFile,
#                       app_settings: Settings = Depends(get_settings)):
    
#     # validate the file properties
#     is_valid, result_signal = validate_uploaded_file(file=file)

#     return {
#         "signal": result_signal
#     }