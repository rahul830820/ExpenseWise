from enum import Enum


class DashboardPeriod(str, Enum):
    MONTH = "month"
    LAST_MONTH = "last_month"
    LAST_3_MONTHS = "last_3_months"
    LAST_6_MONTHS = "last_6_months"
    YEAR = "year"
    ALL = "all"