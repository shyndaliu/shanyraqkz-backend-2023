from fastapi import Depends, Response
from pydantic import Field

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class GetFavoritesResponse(AppModel):
    shanyraks: list


@router.get("/users/favorites/shanyraks", response_model=GetFavoritesResponse)
def get_my_favorites(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    response = svc.repository.get_favorites(user_id=jwt_data.user_id)
    return GetFavoritesResponse(shanyraks=response)
