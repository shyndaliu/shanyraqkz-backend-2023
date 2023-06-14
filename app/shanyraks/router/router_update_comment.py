from fastapi import Depends, HTTPException, status, Response
from typing import Any
from app.utils import AppModel
from pydantic import Field
from ..service import Service, get_service
from . import router

from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data


class UpdateCommentRequest(AppModel):
    content: str


class UpdateCommentResponse(AppModel):
    content: str


@router.post("/{id}/comments/{comment_id}", response_model=UpdateCommentResponse)
def update_comment(
    id: str,
    comment_id: str,
    input: UpdateCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    updated_comment = svc.repository.update_comment(
        id=id, comment_id=comment_id, user_id=jwt_data.user_id, input=input.dict()
    )
    return UpdateCommentResponse(content=updated_comment)
