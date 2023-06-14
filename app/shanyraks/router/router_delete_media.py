from fastapi import Depends, Response, UploadFile
from app.utils import AppModel
from ..service import Service, get_service
from . import router
from typing import List

from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data


class DeleteMediaRequest(AppModel):
    media: list


@router.delete("/{id}/media")
def delete_media(
    id: str,
    input: DeleteMediaRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    svc.repository.delete_media(id=id, user_id=jwt_data.user_id, input=input.dict())
    return Response(status_code=200)
