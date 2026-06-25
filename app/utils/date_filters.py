from datetime import date

from dateutil.relativedelta import relativedelta

from app.schemas.dashboard_period import DashboardPeriod


def get_period_dates(period: DashboardPeriod):
    today = date.today()

    start_date = None
    end_date = today

    if period == DashboardPeriod.MONTH:
        start_date = today.replace(day=1)

    elif period == DashboardPeriod.LAST_MONTH:
        first_day_this_month = today.replace(day=1)

        end_date = first_day_this_month - relativedelta(days=1)

        start_date = end_date.replace(day=1)

    elif period == DashboardPeriod.LAST_3_MONTHS:
        start_date = (
            today.replace(day=1)
            - relativedelta(months=2)
        )

    elif period == DashboardPeriod.LAST_6_MONTHS:
        start_date = (
            today.replace(day=1)
            - relativedelta(months=5)
        )

    elif period == DashboardPeriod.YEAR:
        start_date = date(today.year, 1, 1)

    elif period == DashboardPeriod.ALL:
        start_date = None

    return start_date, end_date