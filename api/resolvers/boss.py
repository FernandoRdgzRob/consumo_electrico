from operator import itemgetter
import os
from app import db
from api.models.role import Role
from api.models.hitman import Hitman
from api.models.manager import Manager
from api.models.user import User
from .utils.authorization import check_is_boss

MANAGER_ROLE = os.getenv("MANAGER_ROLE")
Session = db.sessionmaker(bind=db.engine)
ROLE = "role_id"
MANAGER = "manager"
SUCCESS = "success"
ERRORS = "errors"
NOT_ALLOWED_TO_PROMOTE_ERROR = "You are not allowed to promote users"


def promote_hitman(_obj, info, data):
    try:
        user_id = itemgetter("id")(data)
        [is_allowed, _user] = check_is_boss(info.context)
        if is_allowed:
            session = Session()

            with session.begin():
                hitman = Hitman.query.filter_by(id=user_id).first()
                user = User.query.filter_by(id=user_id).first()
                role = Role.query.filter_by(name=MANAGER_ROLE).first()

                if hitman is not None and user is not None:
                    user.role = role
                    hitman.manager = None
                    manager = Manager(hitman=hitman)
                    return {
                        MANAGER: manager.to_dict(),
                        SUCCESS: True
                    }
        return {
            SUCCESS: False,
            ERRORS: [NOT_ALLOWED_TO_PROMOTE_ERROR]
        }
    except Exception as error:
        return {
            SUCCESS: False,
            ERRORS: [str(error)]
        }
