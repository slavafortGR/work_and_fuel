from flask import flash
from datetime import datetime, timedelta


def validate_create_work_form(date_str, route_number, locomotive_number, start_of_work,
                              end_of_work, beginning_fuel_liters,
                              end_fuel_litres, specific_weight
                              ):
    errors = []

    try:
        datetime.strptime(date_str, '%Y.%m.%d')
    except ValueError:
        errors.append(f'Неверный формат даты ({date_str}). Используйте ГГГГ.ММ.ДД.')

    for time_str in [start_of_work, end_of_work]:
        try:
            datetime.strptime(time_str, '%H:%M')
        except ValueError:
            errors.append(f'Неверный формат времени ({time_str}). Используйте ЧЧ:ММ.')

    for field_name, value in {
        'Номер маршрута': route_number,
        'Номер локомотива': locomotive_number
    }.items():
        if not value.isdigit():
            errors.append(f'Ошибка: {field_name} должен быть целым числом.')

    for field_name, value in {
        'Дизельное топливо принял': beginning_fuel_liters,
        'Дизельное топливо сдал': end_fuel_litres,
        'Удельный вес топлива': specific_weight,
    }.items():
        try:
            float(value)
        except ValueError:
            errors.append(f'Ошибка: {field_name} должен быть числом.')

    try:
        start_time = datetime.strptime(start_of_work, '%H:%M')
        end_time = datetime.strptime(end_of_work, '%H:%M')

        if end_time < start_time:
            end_time += timedelta(days=1)

        if end_time - start_time < timedelta(hours=3):
            errors.append('Продолжительность смены не может быть менее трёх (3) часов.')
    except ValueError:
        errors.append('Ошибка при вычислении времени работы.')

    return errors


def validate_settings_form(
        park_l_norm, park_g_norm, park_e_norm,
        park_z_norm, park_vm_norm, park_nijny_norm,
        park_vchd_3_norm, park_tch_1_norm, park_tch_8_norm,
        park_dnepr_norm, park_gorvetka_norm, park_diyovka_norm,
        park_goryainovo_norm, park_kaidakskaya_norm, park_pristan_norm,
        park_nizhnedneprovsk_norm, hot_state, cool_state
):
    if not (10 <= float(park_l_norm) <= 20):
        flash('Проверьте корректность ввода! Норма работы парка "Л" должна быть в диапазоне от 10 до 20 кг.', 'danger')
        return False

    if not (10 <= float(park_g_norm) <= 20):
        flash('Проверьте корректность ввода! Норма работы парка "Г" должна быть в диапазоне от 10 до 20 кг.', 'danger')
        return False

    if not (10 <= float(park_e_norm) <= 20):
        flash('Проверьте корректность ввода! Норма работы парка "Е" должна быть в диапазоне от 10 до 20 кг.', 'danger')
        return False

    if not (10 <= float(park_z_norm) <= 20):
        flash('Проверьте корректность ввода! Норма работы парка "З" должна быть в диапазоне от 10 до 20 кг.', 'danger')
        return False

    if not (10 <= float(park_vm_norm) <= 20):
        flash('Проверьте корректность ввода! Норма работы парка "Втормет" должна быть в диапазоне от 10 до 20 кг.',
              'danger')
        return False

    if not (10 <= float(park_nijny_norm) <= 20):
        flash('Проверьте корректность ввода! Норма работы парка "Нижний" должна быть в диапазоне от 10 до 20 кг.',
              'danger')
        return False

    if not (10 <= float(park_vchd_3_norm) <= 20):
        flash('Проверьте корректность ввода! Норма работы парка "ВЧД-3" должна быть в диапазоне от 10 до 20 кг.',
              'danger')
        return False

    if not (10 <= float(park_tch_1_norm) <= 15):
        flash('Проверьте корректность ввода! Норма работы депо "ТЧ-1" должна быть в диапазоне от 10 до 15 кг.',
              'danger')
        return False

    if not (10 <= float(park_tch_8_norm) <= 15):
        flash('Проверьте корректность ввода! Норма работы депо "ТЧ-8" должна быть в диапазоне от 10 до 15 кг.',
              'danger')
        return False

    if not (10 <= float(park_dnepr_norm) <= 20):
        flash('Проверьте корректность ввода! Норма работы парка "Днепр Главный" должна быть в диапазоне от 10 до 20 кг.',
              'danger')
        return False

    if not (10 <= float(park_gorvetka_norm) <= 20):
        flash('Проверьте корректность ввода! Норма работы парка "Горветка" должна быть в диапазоне от 10 до 20 кг.',
              'danger')
        return False

    if not (10 <= float(park_diyovka_norm) <= 20):
        flash('Проверьте корректность ввода! Норма работы парка "Диёвка" должна быть в диапазоне от 10 до 20 кг.',
              'danger')
        return False

    if not (10 <= float(park_goryainovo_norm) <= 20):
        flash('Проверьте корректность ввода! Норма работы парка "Горяиново" должна быть в диапазоне от 10 до 20 кг.',
              'danger')
        return False

    if not (10 <= float(park_kaidakskaya_norm) <= 20):
        flash('Проверьте корректность ввода! Норма работы парка "Кайдакская" должна быть в диапазоне от 10 до 20 кг.',
              'danger')
        return False

    if not (10 <= float(park_nizhnedneprovsk_norm) <= 20):
        flash('Проверьте корректность ввода! Норма работы парка "Нижнеднепровск" должна быть в диапазоне от 10 до 20 кг.',
              'danger')
        return False

    if not (10 <= float(park_pristan_norm) <= 20):
        flash('Проверьте корректность ввода! Норма работы парка "Н.Д.Пристань" должна быть в диапазоне от 10 до 20 кг.',
              'danger')
        return False

    if int(hot_state) != 10:
        flash('Проверьте корректность ввода! Норма для простоя в "Горячем состоянии" должна быть равной 10 кг.',
              'danger')
        return False

    if int(cool_state) != 0:
        flash(
            'Проверьте корректность ввода! "Простой в холодном состоянии" может иметь исключительно нулевое значение.',
            'danger')
        return False

    return True


def validate_register_form(personnel_number, password):
    if not isinstance(personnel_number, int) or not (10000 <= personnel_number <= 99999):
        flash('Табельный номер должен состоять ровно из 5-ти цифр!', 'danger')
        return False

    if len(password) < 3:
        flash('Пароль должен быть не менее 3-символов!', 'danger')
        return False

    return True


def validate_data_form(route_number, locomotive_number,
                       beginning_fuel_liters, end_fuel_litres,
                       specific_weight
                       ):
    if not route_number.isdigit() or len(route_number) != 7:
        flash('Номер маршрута должен состоять ровно из 7 цифр.', 'danger')
        return False

    if not locomotive_number.isdigit() or not (3 <= len(locomotive_number) <= 4):
        flash('Номер локомотива должен быть трёхзначным либо четырехзначным числом.', 'danger')
        return False

    if not beginning_fuel_liters.isdigit() or not (0 <= int(beginning_fuel_liters) <= 6000):
        flash('Объём дизельного топлива (приёмка) может быть от 0 до 6000 л.', 'danger')
        return False

    if not end_fuel_litres.isdigit() or not (0 <= int(end_fuel_litres) <= 6000):
        flash('Объём дизельного топлива (сдача) может быть от 0 до 6000 л.', 'danger')
        return False

    specific_weight_float = float(specific_weight)
    if not (0.8000 <= specific_weight_float <= 0.8999):
        flash('Переводной коэффициент Д/Т должен быть в диапазоне 0.8000 - 0.8999', 'danger')
        return False

    return True


def convert_to_decimal_hours(time_str):
    if not time_str or ':' not in time_str:
        raise ValueError(f'Некорректный формат времени: "{time_str}" (ожидается "часы:минуты")')

    hours, minutes = map(int, time_str.split(':'))
    decimal_hours = hours + round((minutes * 100 / 60) / 100, 2)
    return decimal_hours


def calculate_work_duration(start_of_work, end_of_work):
    fmt = '%H:%M'
    start_of_work = datetime.strptime(start_of_work, fmt)
    end_of_work = datetime.strptime(end_of_work, fmt)

    if end_of_work < start_of_work:
        end_of_work = end_of_work.replace(day=start_of_work.day + 1)

    work_duration = (end_of_work - start_of_work).seconds / 3600
    return round(work_duration, 2)


def validate_work_time(start_of_work, end_of_work, entered_times):
    actual_work_time = calculate_work_duration(start_of_work, end_of_work)
    print('DEBUG: entered_times =', entered_times, type(entered_times))
    if all(isinstance(t, float) for t in entered_times):
        entered_work_time = sum(entered_times)
    else:
        entered_work_time = sum(convert_to_decimal_hours(t) for t in entered_times)

    if entered_work_time < actual_work_time:
        raise ValueError(
            f'Ошибка! Введённое рабочее время ({entered_work_time} ч) меньше фактического ({actual_work_time} ч)')

    return True


def get_park_norms(settings):
    park_keys = [
        'park_l_norm', 'park_g_norm', 'park_e_norm', 'park_z_norm',
        'park_vm_norm', 'park_nijny_norm', 'park_vchd_3_norm', 'park_tch_1_norm',
        'park_tch_8_norm', 'park_dnepr_norm', 'park_gorvetka_norm','park_diyovka_norm',
        'park_goryainovo_norm', 'park_kaidakskaya_norm', 'park_nizhnedneprovsk_norm',
        'park_pristan_norm', 'hot_state', 'cool_state'
    ]
    return {i + 1: getattr(settings, key) for i, key in enumerate(park_keys)}
