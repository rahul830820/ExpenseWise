from datetime import date

from pydantic import BaseModel, Field


class IncomeCreate(BaseModel):

    amount: float = Field(
        gt=0
    )

    source: str = Field(
        min_length=2,
        max_length=255
    )

    income_date: date


class IncomeResponse(BaseModel):

    id: int

    amount: float

    source: str

    income_date: date

    class Config:
        from_attributes = True