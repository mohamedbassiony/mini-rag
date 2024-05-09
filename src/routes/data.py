from fastapi import FastAPI, APIRouter, Depends, UploadFile
import os
from helpers.config import get_settings, Settings
from controllers.DataController import DataController
from controllers import DataController

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)

# @data_router.post("/upload/{project_id}")
# async def upload_data(project_id: str, file: UploadFile,
#                       app_settings: Settings = Depends(get_settings)):
    
#     # validate the file properties
#     is_valid = DataController().validate_uploaded_file(file=file)

#     return is_valid


def validate_uploaded_file(file: UploadFile):
    FILE_ALLOWED_TYPES=["text/plain", "application/pdf"]
    FILE_MAX_SIZE=10
    size_scale = 1048576 # convert MB to bytes


    if file.content_type not in FILE_ALLOWED_TYPES:
        return False
    
    if file.size > FILE_MAX_SIZE * size_scale:
        return False
    
    return True

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    
    # validate the file properties
    is_valid = validate_uploaded_file(file=file)

    return is_valid