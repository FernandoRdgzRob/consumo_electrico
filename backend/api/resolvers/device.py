from api import db
from ..models.device import Device
from ..models.consumption import Consumption

from .utils.authorization import get_user_from_token, check_if_user_is_allowed
from .utils.basic_requests import (
    handle_create_instance,
    handle_update_instance,
)
from .utils.consumptions_generator import consumptions_dictionary, generate_consumptions
from ..exceptions.not_found import UserNotFound
from ..exceptions.not_allowed import UserNotAllowed
from ..const import READ
import os

def get_devices_from_user(_obj, info):
    module_name = os.path.basename(__file__)[:-3]

    try:
        user = get_user_from_token(request=info.context)

        is_user_allowed = check_if_user_is_allowed(
            role=user.role, permit=READ, module_name=module_name
        )

        if not is_user_allowed:
            raise UserNotAllowed()

        devices = Device.query.filter_by(user=user)

        payload = {
            "success": True,
            "devices": devices,
        }

    except Exception as error:
        payload = {"success": False, "errors": [str(error)]}

    return payload


def upsert_device(_obj, info, data):
    # Permits are based on the module name, which is unique on the db. We use the file name as equivalence to the
    # module we are retrieving from db
    module_name = os.path.basename(__file__)[:-3]

    try:
        user = get_user_from_token(request=info.context)
        if user is not None:
            if data.get("device_id") is not None:
                # Fields that can be updated, if others are sent, error will be returned
                accepted_keys = {
                    "device_id",
                    "name",
                    "min_c",
                    "max_c",
                    "average_consumption",
                    "sort",
                    "freq_time",
                    "turn_off",
                    "metering",
                }
                device = handle_update_instance(
                    user=user,
                    module_name=module_name,
                    data=data,
                    accepted_keys=accepted_keys,
                    model=Device,
                    id_from_record=data.get("device_id"),
                    id_key="device_id"
                )
            else:
                # Fields that are mandatory to create a new device
                desired_keys = {
                    "name",
                    "type",
                    "min_c",
                    "max_c",
                    "average_consumption",
                    "sort",
                    "freq_time",
                    "turn_off",
                    "metering",
                }

                data["user"] = user

                device = handle_create_instance(
                    user=user,
                    module_name=module_name,
                    data=data,
                    desired_keys=desired_keys,
                    model=Device,
                )

                if consumptions_dictionary.get(device.type):
                    consumptions = generate_consumptions(device_name=device.type, days=2)
                    for consumption_data in consumptions:
                        consumption_data["device"] = device
                        consumption = Consumption(fields_map=consumption_data)
                        db.session.add(consumption)
                    db.session.commit()

            payload = {"device": device, "success": True}
        else:
            raise UserNotFound()

    except Exception as error:
        payload = {"success": False, "errors": [str(error)]}

    return payload
