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
        return existing_shift is not None


PARK_NAMES = {
    "1": 'Парк "Л"', "2": 'Парк "Г"', "3": 'Парк "Е"', "4": 'Парк "З"',
    "5": 'Парк "Втормет"', "6": 'Парк "Нижний"', "7": 'Парк "ВЧД-3"',
    "8": 'Парк "ТЧ-1"', "9": 'Парк "ТЧ-8"', "10": 'Парк "Днепр Главный"',
    "11": 'Парк "Горветка"', "12": 'Парк "Диёвка"', "13": 'Парк "Горяиново"',
    "14": 'Парк "Кайдакская"', "15": 'Парк "Нижнеднепровск"',
    "16": 'Парк "Н.Д. Пристань"', "17": 'Парк "Лотсманка"', "18": 'Парк "Встречный"',
    "19": 'Парк "Днепр Грузовой"', "20": 'Парк "Обводная"', "21": 'Парк "Лиски"',
    "22": 'Парк "Привольное"', "23": 'Парк "Рясная"', "24": 'Парк "Сухачёвка"',
    "25": 'Горячий простой', "26": 'Холодный простой'
}
