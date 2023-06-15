from fastapi import Depends, Response, UploadFile
from app.utils import AppModel
from ..service import Service, get_service
from . import router

from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data


@router.post("/users/avatar")
def upload_avatar(
    file: UploadFile,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    url = svc.s3_service.upload_file(file.file, file.filename)
    svc.repository.upload_avatar(user_id=jwt_data.user_id, url=url)
    return Response(status_code=200)
