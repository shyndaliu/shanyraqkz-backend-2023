from fastapi import Depends, Response, UploadFile
from app.utils import AppModel
from ..service import Service, get_service
from . import router
from typing import List

from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data


@router.post("/{id}/media")
def add_media(
    id: str,
    files: List[UploadFile],
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    media_urls = []
    for file in files:
        media_urls.append(svc.s3_service.upload_file(file.file, file.filename))
    svc.repository.add_media(id=id, user_id=jwt_data.user_id, urls=media_urls)
    return Response(status_code=200)
