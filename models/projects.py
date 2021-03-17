from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class ProjectRequestModel(BaseModel):
    title: str
    description: Optional[str] = None
    owner: str
    tags: List[str]


class ProjectResponseModel(ProjectRequestModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    active: bool
