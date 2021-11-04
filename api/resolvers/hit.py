import os
from operator import itemgetter
from datetime import datetime
from api.models.hit import Hit
from app import db
from .utils.authorization import check_can_get_hits, check_can_get_hits_assigned_to_itself, check_can_create_hit

DEFAULT_CREATION_ERROR = "You are not authorized to create a new hit"
HITS = "hits"
HIT = "hit"
SUCCESS = "success"
ERRORS = "errors"
DEFAULT_STATUS = "CREATED"
BOSS_ROLE = os.getenv("BOSS_ROLE")
MANAGER_ROLE = os.getenv("MANAGER_ROLE")

GET_HITS_AUTHORIZATION_ERR0R = "You do not have permission to retrieve hits"


def get_hits(_obj, info):
    try:
        [can_get_hits, user, role] = check_can_get_hits(info.context)
        if can_get_hits:
            if role == BOSS_ROLE:
                hits_from_query = Hit.query.all()

                hits = map(lambda hit: hit.to_dict(), hits_from_query)

                return {
                    HITS: hits,
                    SUCCESS: True
                }
            elif role == MANAGER_ROLE:
                hits_from_query = Hit.query.filter_by(creator=user).all()

                hits = map(lambda hit: hit.to_dict(), hits_from_query)

                return {
                    HITS: hits,
                    SUCCESS: True
                }

        return {
            SUCCESS: False,
            ERRORS: [GET_HITS_AUTHORIZATION_ERR0R]
        }
    except Exception as error:
        return {
            SUCCESS: False,
            ERRORS: [str(error)]
        }


def get_hits_assigned_to_me(_obj, info):
    try:
        [is_user_allowed, hitman] = check_can_get_hits_assigned_to_itself(info.context)

        if is_user_allowed:
            hits_from_query = Hit.query.filter_by(hitman=hitman).all()

            return {
                SUCCESS: True,
                HITS: map(lambda hit: hit.to_dict(), hits_from_query),
            }
    except Exception as error:
        return {
            SUCCESS: False,
            ERRORS: [str(error)]
        }


def create_hit(_obj, info, data):
    try:
        [is_user_allowed, user] = check_can_create_hit(info.context)

        if is_user_allowed:
            target_name, description = itemgetter("targetName", "description")(data)
            creation_date = datetime.today().date()

            new_hit = Hit(target_name=target_name, creation_date=creation_date, description=description, creator=user,
                          status=DEFAULT_STATUS)

            db.session.add(new_hit)
            db.session.commit()

            return {
                SUCCESS: True,
                HIT: new_hit.to_dict()
            }

        return {
            SUCCESS: False,
            ERRORS: [str(DEFAULT_CREATION_ERROR)]
        }
    except Exception as error:
        return {
            SUCCESS: False,
            ERRORS: [str(error)]
        }
