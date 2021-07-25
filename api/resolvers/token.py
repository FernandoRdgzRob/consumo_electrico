import jwt
import os
import datetime

TOKEN = "token"
EXPIRATION_DATE = "exp"
ID = "public_id"
DEFAULT = os.getenv("DEFAULT_IDENTIFIER")
TOKEN_EXPIRATION_SPAN = int(os.getenv("TOKEN_EXPIRATION_SPAN"))
VALUE = "value"
APP_SECRET = os.getenv("APP_SECRET")


def generate_token(user_id):
    if user_id is None:
        return

    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRATION_SPAN)

    token = jwt.encode({ID: user_id, EXPIRATION_DATE: expiration_date},
                       APP_SECRET)

    return [token.decode('UTF-8'), expiration_date]
