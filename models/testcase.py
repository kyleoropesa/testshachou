from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import datetime
from uuid import UUID
from config.errormessage import ErrorsConfig

ERRORS_CONF = ErrorsConfig()


class TestCaseRequestModel(BaseModel):
    title: str
    description: str
    author: str
    tags: Optional[List[str]]
    expected_results: str

    @validator('title', 'description', 'author', 'expected_results')
    def fields_should_not_be_space_only(cls, value: str):
        if value.isspace():
            raise ValueError(ERRORS_CONF.FIELD_VALUE.SPACES_ONLY)
        else:
            return value

    @validator('title', 'description', 'author', 'expected_results')
    def fields_should_not_be_empty_string(cls, value: str):
        if value == "":
            raise ValueError(ERRORS_CONF.FIELD_VALUE.EMPTY_STRINGS)
        else:
            return value

    @validator('tags')
    def tag_values_should_not_be_empty_string(cls, tag_list: str):
        for tags in tag_list:
            if tags == "":
                raise ValueError(ERRORS_CONF.FIELD_VALUE.EMPTY_STRINGS)
        return tag_list

    @validator('tags')
    def tag_values_should_not_be_space_only(cls, tag_list: str):
        for tags in tag_list:
            if tags.isspace():
                raise ValueError(ERRORS_CONF.FIELD_VALUE.SPACES_ONLY)
        return tag_list


class TestCaseResponseModel(TestCaseRequestModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    updated_by: str
