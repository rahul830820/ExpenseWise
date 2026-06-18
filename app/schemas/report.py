from pydantic import BaseModel


class CategoryWiseReport(BaseModel):
    category: str
    total: float


class MonthlyReport(BaseModel):
    month: str
    total: float


class TopCategoryReport(BaseModel):
    category: str
    total: float
