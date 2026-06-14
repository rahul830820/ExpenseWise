from pydantic import BaseModel


class MonthlyReport(BaseModel):
    month: str
    total: float