from fastapi import Depends, HTTPException, status, Response
from typing import Any
from app.utils import AppModel
from pydantic import Field
from ..service import Service, get_service
from . import router


class GetCommentResponse(AppModel):
    comments: list


@router.get("/{id}/comments", response_model=GetCommentResponse)
def get_all_comments(
    id: str,
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    all_comments = svc.repository.get_comments(id=id)
    if all_comments == None:
        return GetCommentResponse(comments=[])
    return GetCommentResponse(comments=all_comments)
