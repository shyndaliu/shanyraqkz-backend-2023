from fastapi import Depends, Response, UploadFile
from app.utils import AppModel
from ..service import Service, get_service
from . import router

from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data


@router.delete("/users/avatar")
def delete_avatar(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    svc.repository.delete_avatar(user_id=jwt_data.user_id)
    return Response(status_code=200)
