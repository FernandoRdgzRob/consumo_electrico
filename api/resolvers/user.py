import os
from api.models.user import User
from api.models.role import Role
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from operator import itemgetter
from .token import generate_token

DEFAULT_ROLE = "DEFAULT"
SUCCESS = "success"
ERRORS = "errors"
USER = "user"
HITMAN = "hitman"
TOKEN = "token"
VALUE = "value"
EXPIRATION_DATE = "expirationDate"
ID = "id"
TOKEN_EXPIRATION_SPAN = int(os.getenv("TOKEN_EXPIRATION_SPAN"))
APP_SECRET = os.getenv("APP_SECRET")
CREDENTIALS_NOT_VALID_ERROR = "The credentials provided are not valid"


def login(obj, info, data):
    email, password = itemgetter("email", "password")(data)
    try:
        user = User.query.filter_by(email=email).first()

        if user is not None and check_password_hash(user.password, password):
            [value, expiration_date] = generate_token(user_id=user.id)

            payload = {
                SUCCESS: True,
                USER: user.to_dict(),
                TOKEN: {VALUE: value, EXPIRATION_DATE: expiration_date},
            }
        else:
            payload = {SUCCESS: False, ERRORS: [CREDENTIALS_NOT_VALID_ERROR]}
    except Exception as error:
        payload = {SUCCESS: False, ERRORS: [str(error)]}

    return payload


def sign_up(obj, info, data):
    name, email, password = itemgetter("name", "email", "password")(data)

    try:
        hashed_password = generate_password_hash(
            password, method="sha256", salt_length=16
        )

        role = Role.query.filter_by(default=DEFAULT_ROLE).first()
        creation_date = datetime.today().date()
        new_user = User(
            name=name,
            email=email,
            creation_date=creation_date,
            password=hashed_password,
            role=role,
        )
        db.session.add(new_user)
        db.session.commit()

        [value, expiration_date] = generate_token(user_id=new_user.id)

        payload = {
            SUCCESS: True,
            TOKEN: {VALUE: value, EXPIRATION_DATE: expiration_date},
        }
    except Exception as error:
        payload = {SUCCESS: False, ERRORS: [str(error)]}

    return payload
