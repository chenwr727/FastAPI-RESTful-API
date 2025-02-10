from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    status: str = Field(..., description="Status of the response")
    data: T = Field(..., description="Data of the response")
    message: Optional[str] = Field(None, description="Message of the response")
