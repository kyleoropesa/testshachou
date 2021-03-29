from pydantic import BaseModel


class GeneralError(BaseModel):
    error: str
