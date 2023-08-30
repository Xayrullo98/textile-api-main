from fastapi import HTTPException


def role_verification(user, function):
    # if user.role not in ["admin", "stage_admin", "stage_user", "warehouseman"]:
    #     return True
    allowed_functions_for_stage_admins = []
    allowed_functions_for_stage_users = []
    allowed_functions_for_warehouseman = []
    if user.role == "admin":
        return True
    elif user.role == "stage_admin" and function in allowed_functions_for_stage_admins:
        return True
    elif user.role == "stage_user" and function in allowed_functions_for_stage_users:
        return True
    elif user.role == "warehouseman" and function in allowed_functions_for_warehouseman:
        return True
    raise HTTPException(status_code=401, detail='Sizga ruhsat berilmagan!')

