from pydantic import BaseConfig
from dataclasses import dataclass


class FieldValueErrors(BaseConfig):
    SPACES_ONLY: str = 'Spaces are confusing, use alphanumeric characters instead'
    EMPTY_STRINGS: str = 'Empty strings are not allowed'


class GeneralErrors(BaseConfig):
    PROJECT_DOES_NOT_EXIST: str = "Project ID does not exist"


@dataclass
class ErrorsConfig:
    FIELD_VALUE: FieldValueErrors = FieldValueErrors()
    GENERAL_ERRORS: GeneralErrors = GeneralErrors()
