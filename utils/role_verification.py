from fastapi import HTTPException


def role_verification(user, function):

    allowed_functions_for_stage_admins = ['add_stage_user', 'get_stage_users', 'stage_user_update', 'stage_user_delete']
    allowed_functions_for_stage_users = []
    allowed_functions_for_warehouseman = ['get_supplies', 'get_suppliers', 'confirm_supply']
    if user.role == "admin":
        return True
    elif user.role == "stage_admin" and function in allowed_functions_for_stage_admins:
        return True
    elif user.role == "stage_user" and function in allowed_functions_for_stage_users:
        return True
    elif user.role == "warehouseman" and function in allowed_functions_for_warehouseman:
        return True
    raise HTTPException(status_code=400, detail='Sizga ruhsat berilmagan!')

