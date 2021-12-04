from ..models.module import Module
from .utils.authorization import get_user_from_token
from .utils.basic_requests import (
    handle_create_instance,
    handle_update_instance,
    handle_get_all_instances,
)
from ..exceptions.not_found import UserNotFound
import os


def get_modules(_obj, info):
    module_name = os.path.basename(__file__)[:-3]

    try:
        user = get_user_from_token(request=info.context)
        modules = handle_get_all_instances(
            user=user, module_name=module_name, model=Module
        )
        payload = {
            "success": True,
            "modules": modules,
        }

    except Exception as error:
        payload = {"success": False, "errors": [str(error)]}

    return payload


def upsert_module(_obj, info, data):
    # Permits are based on the module name, which is unique on the db. We use the file name as equivalence to the
    # module we are retrieving from db
    module_name = os.path.basename(__file__)[:-3]

    try:
        user = get_user_from_token(request=info.context)
        if user is not None:
            if data.get("module_id") is not None:
                # Fields that can be updated, if others are sent, error will be returned
                accepted_keys = {"name", "module_id"}
                module = handle_update_instance(
                    user=user,
                    module_name=module_name,
                    data=data,
                    accepted_keys=accepted_keys,
                    model=Module,
                    id_from_record=data.get("module_id"),
                    id_key="module_id"
                )
            else:
                # Fields that are mandatory to create a new device
                desired_keys = {"name"}

                module = handle_create_instance(
                    user=user,
                    module_name=module_name,
                    data=data,
                    desired_keys=desired_keys,
                    model=Module,
                )

            payload = {"module": module, "success": True}
        else:
            raise UserNotFound()

    except Exception as error:
        payload = {"success": False, "errors": [str(error)]}

    return payload
