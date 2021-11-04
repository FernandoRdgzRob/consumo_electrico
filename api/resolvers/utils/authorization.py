import jwt
import os
from api.models.user import User
from api.models.hitman import Hitman

ID = "public_id"
APP_SECRET = os.getenv("APP_SECRET")
HITMAN_ROLE = os.getenv("HITMAN_ROLE")
MANAGER_ROLE = os.getenv("MANAGER_ROLE")
BOSS_ROLE = os.getenv("BOSS_ROLE")


def check_is_hitman(request):
    try:
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
            token_data = jwt.decode(token, APP_SECRET)

            user = User.filter_by(id=token_data[ID]).first()

            return user.role.name == HITMAN_ROLE

        return False
    except Exception as error:
        print(error)
        return False


def check_can_get_hits(request):
    try:
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
            token_data = jwt.decode(token, APP_SECRET)
            user = User.query.filter_by(id=token_data[ID]).first()

            is_allowed = user.role.name == MANAGER_ROLE or user.role.name == BOSS_ROLE

            return [is_allowed, user, user.role.name]

        return [False, None, None]
    except Exception as error:
        print(error)
        return [False, None, None]


def check_can_get_hits_assigned_to_itself(request):
    try:
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
            token_data = jwt.decode(token, APP_SECRET)
            user = User.query.filter_by(id=token_data[ID]).first()

            is_user_allowed = user.role.name == MANAGER_ROLE or user.role.name == HITMAN_ROLE

            if is_user_allowed:
                hitman = Hitman.query.filter_by(user=user).first()

                if hitman is not None:
                    return [is_user_allowed, hitman]

            return [is_user_allowed, None]

        return [False, None]
    except Exception as error:
        print(error)
        return [False, None]


def check_can_create_hit(request):
    return check_is_boss_or_manager(request)


def check_is_boss(request):
    try:
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
            token_data = jwt.decode(token, APP_SECRET)
            user = User.query.filter_by(id=token_data[ID]).first()

            is_user_allowed = user.role.name == BOSS_ROLE

            return [is_user_allowed, user]

        return [False, None]
    except Exception as error:
        print(error)
        return [False, None]


def check_is_boss_or_manager(request):
    try:
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
            token_data = jwt.decode(token, APP_SECRET)
            user = User.query.filter_by(id=token_data[ID]).first()

            is_user_allowed = user.role.name == MANAGER_ROLE or user.role.name == BOSS_ROLE

            return [is_user_allowed, user]

        return [False, None]
    except Exception as error:
        print(error)
        return [False, None]
