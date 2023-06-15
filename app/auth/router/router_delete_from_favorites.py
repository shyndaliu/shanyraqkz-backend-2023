from fastapi import Depends, Response
from pydantic import Field

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


@router.delete("/users/favorites/shanyraks/{id}")
def delete_from_favorites(
    id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    svc.repository.delete_from_favorites(id=id, user_id=jwt_data.user_id)
    return Response(status_code=200)
