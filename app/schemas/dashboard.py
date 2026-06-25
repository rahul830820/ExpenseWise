from pydantic import BaseModel
from datetime import date

class DashboardSummary(BaseModel):

    total_income: float

    total_expenses: float

    savings: float

    savings_rate: float

    expense_count: int

    category_count: int

class RecentExpense(BaseModel):

    id: int

    description: str

    amount: float

    expense_date: date

    class Config:
        from_attributes = True