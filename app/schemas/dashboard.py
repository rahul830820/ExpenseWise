from pydantic import BaseModel


class DashboardSummary(BaseModel):

    total_expenses: float

    expense_count: int

    category_count: int