from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import datetime
from uuid import UUID


class TestCaseRequestModel(BaseModel):
    title: str
    description: str
    author: str
    tags: Optional[List[str]]
    expected_results: str

    @validator('title', 'description', 'author', 'expected_results')
    def fields_should_not_be_space_only(cls, value: str):
        if value.isspace():
            raise ValueError('Spaces are confusing, use alphanumeric characters instead')
        else:
            return value



class TestCaseResponseModel(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    updated_by: str
