from typing import Optional, List

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool
    data: Optional[object] = []


class ErrorResponse(BaseModel):
    success: bool = False
    errors: List[object] = []
