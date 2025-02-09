from datetime import datetime, timedelta

from sqlalchemy import and_
from workfuel.models import WorkTime

def get_monthly_work_time(user_id):
    now = datetime.now()
    first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)

    work_shifts = WorkTime.query.filter(
        and_(
            WorkTime.user_id == user_id,
            WorkTime.end_of_work >= first_day,
            WorkTime.start_of_work >= first_day - timedelta(days=1)
        )
    ).all()

    total_work_time = timedelta()
    for shift in work_shifts:
        shift_start = shift.start_of_work
        shift_end = shift.end_of_work

        if shift_start.date() == last_day.date():
            continue

        if shift_start.date() == (first_day - timedelta(days=1)).date():

            total_work_time += shift_end - shift_start
            continue

        if shift_start >= first_day:
            total_work_time += shift_end - shift_start

    hours, remainder = divmod(total_work_time.total_seconds(), 3600)
    minutes = remainder // 60
    formatted_time = f"{int(hours):02}:{int(minutes):02}"

    return formatted_time


def existing_work_time(user_id, start_of_work, end_of_work):
    existing_shift = WorkTime.query.filter(
        WorkTime.user_id == user_id,
        WorkTime.start_of_work < end_of_work,
        WorkTime.end_of_work > start_of_work
    ).first()

    if existing_shift:
        return  existing_shift is not None
