from fastapi import Depends, HTTPException, status, Response
from typing import Any
from app.utils import AppModel
from pydantic import Field
from ..service import Service, get_service
from . import router

from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data


class PostCommentRequest(AppModel):
    content: str


@router.post("/{id}/comments")
def post_a_new_comment(
    id: str,
    input: PostCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    new_comment = svc.repository.post_comment(
        id=id, user_id=jwt_data.user_id, input=input.dict()
    )
    return Response(status_code=200)
