from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional

class RequestValidator(BaseModel):
    method: str
    path: str
    body: Optional[str]

    @field_validator('method')
    def validate_method(cls, value):
        if value not in {'GET', 'POST'}:
            raise ValueError('Invalid request method')
        return value

    @field_validator('path')
    def validate_path(cls, value):
        if not value.startswith('/'):
            raise ValueError('Path must start with "/"')
        return value