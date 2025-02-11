from flask import flash
from datetime import datetime, timedelta


def validate_create_work_form(date_str, route_number, locomotive_number, start_of_work,
                              end_of_work, beginning_fuel_liters,
                              end_fuel_litres, specific_weight, norm
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
        "Номер маршрута": route_number,
        "Номер локомотива": locomotive_number
    }.items():
        if not value.isdigit():
            errors.append(f'Ошибка: {field_name} должен быть целым числом.')

    for field_name, value in {
        'Дизельное топливо принял': beginning_fuel_liters,
        'Дизельное топливо сдал': end_fuel_litres,
        'Удельный вес топлива': specific_weight,
        'Норма': norm
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
        park_vchd_3_norm, park_tch_1_norm, hot_state,
        cool_state
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
        flash('Проверьте корректность ввода! Норма работы парка "Втормет" должна быть в диапазоне от 10 до 20 кг.', 'danger')
        return False

    if not (10 <= float(park_nijny_norm) <= 20):
        flash('Проверьте корректность ввода! Норма работы парка "Нижний" должна быть в диапазоне от 10 до 20 кг.', 'danger')
        return False

    if not (10 <= float(park_vchd_3_norm) <= 20):
        flash('Проверьте корректность ввода! Норма работы парка "ВЧД-3" должна быть в диапазоне от 10 до 20 кг.', 'danger')
        return False

    if not (10 <= float(park_tch_1_norm) <= 15):
        flash('Проверьте корректность ввода! Норма работы депо "ТЧ-1" должна быть в диапазоне от 10 до 15 кг.', 'danger')
        return False

    if int(hot_state) != 10:
        flash('Проверьте корректность ввода! Норма для простоя в "Горячем состоянии" должна быть равной 10 кг.', 'danger')
        return False

    if int(cool_state) != 0:
        flash('Проверьте корректность ввода! "Простой в холодном состоянии" может иметь исключительно нулевое значение.', 'danger')
        return False

    return True


def validate_register_form(personnel_number, password):
    if not isinstance(personnel_number, int) or not (10000 <= personnel_number <= 99999):
        flash('Табельный номер должен состоять ровно из 5-ти цифр!', 'danger')
        return False

    if len(password) <3:
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

    if not locomotive_number.isdigit() or not (3 <= len(locomotive_number) <=4):
        flash('Номер локомотива должен быть трёхзначным либо четырехзначным числом.', 'danger')
        return False

    if not beginning_fuel_liters.isdigit() or not (0 <= int(beginning_fuel_liters) <=6000):
        flash('Объём дизельного топлива (приёмка) может быть от 0 до 6000 л.', 'danger')
        return False

    if not end_fuel_litres.isdigit() or not (0 <= int(end_fuel_litres) <=6000):
        flash('Объём дизельного топлива (сдача) может быть от 0 до 6000 л.', 'danger')
        return False


    specific_weight_float = float(specific_weight)
    if not (0.8000 <= specific_weight_float <= 0.8999):
        flash('Переводной коэффициент Д/Т должен быть в диапазоне 0.8000 - 0.8999', 'danger')
        return False

    return True
