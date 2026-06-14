from pydantic import BaseModel, Field


class BudgetCreate(BaseModel):

    amount: float = Field(
        gt=0
    )

    category_id: int


class BudgetResponse(BaseModel):

    id: int

    amount: float

    category_id: int

    class Config:
        from_attributes = True


class BudgetAnalysis(BaseModel):

    category: str

    budget: float

    spent: float

    remaining: float

    status: str