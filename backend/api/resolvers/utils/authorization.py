import jwt
import os
from api.models.user import User
from ...models.authorization import Authorization
from ...models.module import Module

ID = "public_id"
APP_SECRET = os.getenv("APP_SECRET")

# The context of the app is the raw request made to the server


def get_user_from_token(request):
    if "x-access-token" in request.headers:
        token = request.headers["x-access-token"]
        token_data = jwt.decode(token, APP_SECRET)
        user = User.query.filter_by(id=token_data[ID]).first()

        return user
    else:
        return None


def check_single_ownership_of_record(user_to_check, record_to_check):
    if record_to_check is not None:
        user_from_record = record_to_check.user

        if user_from_record is not None and user_from_record == user_to_check:
            return True

    return False


def check_if_user_is_allowed(role, module_name, permit):
    if os.getenv("APP_MODE") == "DEV" or os.getenv("APP_MODE") == "DEV_NO_DEL":
        return True

    module = Module.query.filter_by(name=module_name).first()

    if module is not None:
        authorization = Authorization.query.filter_by(
            module=module, role=role, permit=permit
        ).first()

        if authorization is not None:
            return True

    return False
