from typing import Any

from fastapi import Depends
from pydantic import Field

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class GetShanyraqResponse(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: Any = Field(alias="user_id")


@router.get("/{id}", status_code=200, response_model=GetShanyraqResponse)
def get_shanyraq(id: str, svc: Service = Depends(get_service)) -> dict[str, Any]:
    response = svc.repository.get_shanyraq_by_id(id=id)
    return response
