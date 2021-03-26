from typing import Optional, List
from pydantic import BaseModel, validator

class TestCaseModel(BaseModel):
    title: str
    description: str
    author: str
    tags: List[str]
