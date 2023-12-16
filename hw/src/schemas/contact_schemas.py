import re
from datetime import datetime, date
from pydantic import BaseModel, EmailStr, Field
from typing import Literal


def phone_number_validator(value):
    if not value.isdigit():
        raise ValueError('Phone number must contain only digits.')
    return value


def birth_date_validator(value):
    if len(str(value)) != 10:
        raise ValueError('Birth date must contain exactly 10 characters.')

    if not re.match(r'\d{4}\.\d{2}\.\d{2}|\d{2}\.\d{2}\.\d{4}', str(value)):
        raise ValueError("Incorrect date format. Birth date should be in [YYYY.MM.DD] or [DD.MM.YYYY] format.")

    if re.match(r'\d{4}\.\d{2}\.\d{2}', str(value)):
        return datetime.strptime(str(value), '%Y.%m.%d').date()
    else:
        return datetime.strptime(str(value), '%d.%m.%Y').date()


class ContactSchema(BaseModel):
    first_name: str = Field(min_length=3, max_length=32)
    last_name: str = Field(min_length=3, max_length=32)
    email: EmailStr = Field(min_length=8, max_length=64)
    phone_number: str = Field(max_length=24, validate=phone_number_validator)
    birth_date: date = Field(max_length=10, validate=birth_date_validator)
    crm_status: Literal['operational', 'analitic', 'corporative'] = 'operational'


class ContactUpdateSchema(ContactSchema):
    pass


class ContactResponseSchema(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    crm_status: str

    class Config:
        from_orm = True
