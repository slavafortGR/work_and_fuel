from flask import flash
def validate_settings_form(
        park_l_norm, park_g_norm, park_e_norm,
        park_z_norm, park_vm_norm, park_nijny_norm,
        park_vchd_3_norm, park_tch_1_norm, hot_state,
        cool_state
):

    if float(park_l_norm) <=0:
        flash("Норма работы парка 'Л' не может быть отрицательным числом либо нулевым значением")
        return False

    if float(park_g_norm) <=0:
        flash("Норма работы парка 'Г' не может быть отрицательным числом либо нулевым значением")
        return False

    if float(park_e_norm) <=0:
        flash("Норма работы парка 'Е' не может быть отрицательным числом либо нулевым значением")
        return False

    if float(park_z_norm) <=0:
        flash("Норма работы парка 'З' не может быть отрицательным числом либо нулевым значением")
        return False

    if float(park_vm_norm) <=0:
        flash("Норма работы парка 'Втормет' не может быть отрицательным числом либо нулевым значением")
        return False

    if float(park_nijny_norm) <=0:
        flash("Норма работы парка 'Нижний' не может быть отрицательным числом либо нулевым значением")
        return False

    if float(park_vchd_3_norm) <=0:
        flash("Норма работы парка 'ВЧД-3' не может быть отрицательным числом либо нулевым значением")
        return False

    if float(park_tch_1_norm) <=0:
        flash("Норма работы депо 'ТЧ-1' не может быть отрицательным числом либо нулевым значением")
        return False

    if float(hot_state) <=0:
        flash("Норма для нахождения в 'Горячем состоянии' не может быть отрицательным числом либо нулевым значением")
        return False

    if int(cool_state) !=0 or int(cool_state) < 0:
        flash("'Нахождение в холодном состоянии' может иметь исключительно нулевое число ")
        return False

    return True
