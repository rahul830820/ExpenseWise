from datetime import date

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):

    amount: float = Field(
        gt=0
    )

    description: str = Field(
        min_length=2,
        max_length=255
    )

    expense_date: date

    category_id: int


class ExpenseResponse(BaseModel):

    id: int

    amount: float

    description: str

    expense_date: date

    category_id: int

    class Config:
        from_attributes = True