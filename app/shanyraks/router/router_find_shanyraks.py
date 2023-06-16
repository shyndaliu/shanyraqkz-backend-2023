from typing import Any

from fastapi import Depends, Response
from pydantic import Field

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


@router.get("/")
def find_shanyraks(
    limit: int,
    offset: int,
    type_of: str = "",
    rooms_count: int = 0,
    price_from: int = 0,
    price_until: int = 0,
    svc: Service = Depends(get_service),
):
    result = svc.repository.find_shanyraks(
        limit=limit,
        offset=offset,
        type_of=type_of,
        rooms_count=rooms_count,
        price_from=price_from,
        price_until=price_until,
    )
    return result
