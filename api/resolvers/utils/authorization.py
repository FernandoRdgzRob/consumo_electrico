import jwt
import os
from api.models.user import User

ID = "public_id"
APP_SECRET = os.getenv("APP_SECRET")
HITMAN = os.getenv("HITMAN_ROLE")


def check_is_hitman(request):
    try:
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
            token_data = jwt.decode(token, APP_SECRET)

            user = User.filter_by(id=token_data[ID]).first()

            return user == HITMAN

        return False
    except Exception as error:
        print(error)
        return False
