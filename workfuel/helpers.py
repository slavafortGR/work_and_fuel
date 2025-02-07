from flask import flash
from datetime import datetime, timedelta


def validate_settings_form(
        park_l_norm, park_g_norm, park_e_norm,
        park_z_norm, park_vm_norm, park_nijny_norm,
        park_vchd_3_norm, park_tch_1_norm, hot_state,
        cool_state
):
    if float(park_l_norm) <= 0:
        flash('Проверьте корректность ввода! Норма работы парка "Л" не может быть отрицательным числом либо нулевым значением', 'danger')
        return False

    if float(park_g_norm) <= 0:
        flash('Проверьте корректность ввода! Норма работы парка "Г" не может быть отрицательным числом либо нулевым значением', 'danger')
        return False

    if float(park_e_norm) <= 0:
        flash('Проверьте корректность ввода! Норма работы парка "Е" не может быть отрицательным числом либо нулевым значением', 'danger')
        return False

    if float(park_z_norm) <= 0:
        flash('Проверьте корректность ввода! Норма работы парка "З" не может быть отрицательным числом либо нулевым значением', 'danger')
        return False

    if float(park_vm_norm) <= 0:
        flash('Проверьте корректность ввода! Норма работы парка "Втормет" не может быть отрицательным числом либо нулевым значением', 'danger')
        return False

    if float(park_nijny_norm) <= 0:
        flash('Проверьте корректность ввода! Норма работы парка "Нижний" не может быть отрицательным числом либо нулевым значением', 'danger')
        return False

    if float(park_vchd_3_norm) <= 0:
        flash('Проверьте корректность ввода! Норма работы парка "ВЧД-3" не может быть отрицательным числом либо нулевым значением', 'danger')
        return False

    if float(park_tch_1_norm) <= 0:
        flash('Проверьте корректность ввода! Норма работы депо "ТЧ-1" не может быть отрицательным числом либо нулевым значением', 'danger')
        return False

    if int(hot_state) <= 0:
        flash('Проверьте корректность ввода! Норма для простоя в "Горячем состоянии" не может быть отрицательным либо нулевым значением', 'danger')
        return False

    if int(cool_state) != 0:
        flash('Проверьте корректность ввода! "Простой в холодном состоянии" может иметь исключительно нулевое значение', 'danger')
        return False

    return True


def validate_create_work_form(date_str, route_number, locomotive_number, start_of_work,
                              end_of_work, beginning_fuel_liters,
                              end_fuel_litres, specific_weight, norm
                              ):
    errors = []

    try:
        datetime.strptime(date_str, '%Y.%m.%d')
    except ValueError:
        errors.append(f'Неверный формат даты ({date_str}). Используйте ГГГГ.ММ.ДД')

    for time_str in [start_of_work, end_of_work]:
        try:
            datetime.strptime(time_str, '%H:%M')
        except ValueError:
            errors.append(f'Неверный формат времени ({time_str}). Используйте ЧЧ:ММ')

    for field_name, value in {
        "Номер маршрута": route_number,
        "Номер локомотива": locomotive_number
    }.items():
        if not value.isdigit():
            errors.append(f'Ошибка: {field_name} должен быть целым числом')

    for field_name, value in {
        'Дизельное топливо принял': beginning_fuel_liters,
        'Дизельное топливо сдал': end_fuel_litres,
        'Удельный вес топлива': specific_weight,
        'Норма': norm
    }.items():
        try:
            float(value)
        except ValueError:
            errors.append(f'Ошибка: {field_name} должно быть числом')

    try:
        start_time = datetime.strptime(start_of_work, '%H:%M')
        end_time = datetime.strptime(end_of_work, '%H:%M')

        if end_time < start_time:
            end_time += timedelta(days=1)

        if end_time - start_time < timedelta(hours=3):
            errors.append('Продолжительность смены не может быть менее трёх (3) часов')
    except ValueError:
        errors.append('Ошибка при вычислении времени работы')

    return errors
