from app import db
from ..models.module import Module
from ..const import CREATE, READ
from ..models.role import Role
from ..models.authorization import Authorization
from .utils.authorization import get_user_from_token, check_if_user_is_allowed
from .utils.basic_logic import verify_dict_has_desired_keys
from ..exceptions.not_found import UserNotFound
from ..exceptions.not_allowed import UserNotAllowed
from ..exceptions.bad_request import WrongData
import os


def get_my_authorizations(_obj, info):
    module_name = os.path.basename(__file__)[:-3]

    try:
        user = get_user_from_token(request=info.context)

        if user is None:
            raise UserNotFound(details="User not found")

        is_user_allowed = check_if_user_is_allowed(
            role=user.role, permit=READ, module_name=module_name
        )

        if not is_user_allowed:
            raise UserNotAllowed()

        my_authorizations = Authorization.query.filter_by(role=user.role)

        payload = {
            "success": True,
            "authorizations": my_authorizations,
        }

    except Exception as error:
        payload = {"success": False, "errors": [str(error)]}

    return payload


def create_authorizations(_obj, info, data):
    # Permits are based on the module name, which is unique on the db. We use the file name as equivalence to the
    # module we are retrieving from db
    module_name = os.path.basename(__file__)[:-3]

    try:
        user = get_user_from_token(request=info.context)
        if user is not None:

            is_user_allowed = check_if_user_is_allowed(
                role=user.role, permit=CREATE, module_name=module_name
            )

            if not is_user_allowed:
                raise UserNotAllowed()

            desired_keys = {"module_id", "roles_ids", "permits"}

            data_has_desired_keys = verify_dict_has_desired_keys(
                base_dict=data, desired_keys=desired_keys
            )

            if not data_has_desired_keys:
                raise WrongData(
                    details="Some necessary fields are missing from the request's data"
                )

            module = Module.query.filter_by(id=data.get("module_id")).first()
            permits = data.get("permits")
            roles_ids = data.get("roles_ids")

            if (
                not module
                or not isinstance(roles_ids, list)
                or not isinstance(permits, list)
            ):
                raise WrongData()

            authorizations = []

            for role_id in roles_ids:
                role_to_authorize = Role.query.filter_by(id=role_id).first()
                if not role_to_authorize:
                    raise WrongData(details=f"Role with id {role_id} does not exist")

                for permit in permits:
                    previously_created_authorization = Authorization.query.filter_by(
                        role=role_to_authorize, permit=permit, module=module
                    ).first()

                    if previously_created_authorization is not None:
                        authorizations.append(previously_created_authorization)
                        continue

                    authorization = Authorization(
                        fields_map={
                            "module": module,
                            "role": role_to_authorize,
                            "permit": permit,
                        }
                    )

                    db.session.add(authorization)
                    authorizations.append(authorization)

            db.session.commit()

            payload = {"authorizations": authorizations, "success": True}
        else:
            raise UserNotFound()

    except Exception as error:
        db.session.rollback()
        payload = {"success": False, "errors": [str(error)]}

    return payload
