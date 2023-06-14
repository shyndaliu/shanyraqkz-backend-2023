from fastapi import Depends, HTTPException, status
from typing import Any
from app.utils import AppModel
from pydantic import Field
from ..service import Service, get_service
from . import router

from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data


class CreateShanyrakRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


class CreateShanyrakResponse(AppModel):
    id: str


@router.post(
    "/",
    response_model=CreateShanyrakResponse,
)
def create_new_shanyrak(
    input: CreateShanyrakRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    new_shanyrak_id = svc.repository.create_shanyrak(
        user_id=jwt_data.user_id, shanyrak=input.dict()
    )
    return CreateShanyrakResponse(id=str(new_shanyrak_id))