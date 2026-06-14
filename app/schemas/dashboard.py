from pydantic import BaseModel


class DashboardSummary(BaseModel):

    total_income: float

    total_expenses: float

    savings: float

    savings_rate: float

    expense_count: int

    category_count: int