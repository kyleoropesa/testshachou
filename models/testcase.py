from typing import List
from pydantic import BaseModel, validator
from datetime import datetime
from uuid import UUID


class TestCaseRequestModel(BaseModel):
    title: str
    description: str
    author: str
    tags: List[str]
    expected_results: str


class TestCaseResponseModel(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    updated_by: str
