from fastapi import HTTPException


def role_required(roles: list):

    def checker(current_user):

        if current_user.role not in roles:

            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        return current_user

    return checker