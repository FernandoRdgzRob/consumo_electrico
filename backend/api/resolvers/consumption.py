from ..models.device import Device
from ..models.consumption import Consumption
from ..models.optimized_consumption import OptimizedConsumption
from .utils.authorization import get_user_from_token, check_if_user_is_allowed
from .utils.basic_requests import (
    handle_get_instance_from_user,
)
from ..exceptions.not_found import UserNotFound
from ..exceptions.not_allowed import UserNotAllowed
from ..exceptions.bad_request import WrongData
from ..const import READ, CREATE
from .utils.basic_logic import verify_dict_has_desired_keys
from .utils.authorization import check_if_user_is_allowed
from api import db
from ..heuristic.heuristic import execute_heuristic
import os
import sys
import json

def get_optimized_consumption(device, real_consumption):
    optimized_consumption = execute_heuristic(device=device, real_consumption=real_consumption)

    return {
        "consumption_datetime": real_consumption.consumption_datetime,
        "consumption_amount": optimized_consumption['consumption_amount'],
        "device": device,
    }


def get_consumptions_from_device(_obj, info, data):
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

        desired_keys = {"device_id", "from", "to"}

        device = handle_get_instance_from_user(
            user=user,
            data=data,
            id_from_record=data.get("device_id"),
            desired_keys=desired_keys,
            model=Device,
            module_name=module_name,
        )

        consumptions = Consumption.query.filter(
            (Consumption.device == device)
            & (Consumption.consumption_datetime >= data.get("from"))
            & (Consumption.consumption_datetime <= data.get("to"))
        )

        payload = {"consumptions": consumptions, "success": True}

    except Exception as error:
        payload = {"success": False, "errors": [str(error)]}

    return payload


def get_optimized_consumptions_from_device(_obj, info, data):
    try:
        module_name = os.path.basename(__file__)[:-3]
        user = get_user_from_token(request=info.context)

        if user is None:
            raise UserNotFound(details="User not found")

        desired_keys = {"device_id", "from", "to"}

        device = handle_get_instance_from_user(
            user=user,
            data=data,
            id_from_record=data.get("device_id"),
            desired_keys=desired_keys,
            model=Device,
            module_name=module_name,
        )

        real_consumptions = Consumption.query.filter(
            (Consumption.device == device)
            & (Consumption.consumption_datetime >= data.get("from"))
            & (Consumption.consumption_datetime <= data.get("to"))
        )

        optimized_consumptions = []

        for real_consumption in real_consumptions:
            if real_consumption.optimized_consumption is not None:
                optimized_consumption = real_consumption.optimized_consumption
            else:
                optimized_consumption_data = get_optimized_consumption(
                    device=device, real_consumption=real_consumption
                )

                optimized_consumption = OptimizedConsumption(
                    fields_map=optimized_consumption_data
                )

                real_consumption.optimized_consumption = optimized_consumption

                db.session.add(optimized_consumption)
            optimized_consumptions.append(optimized_consumption)

        db.session.commit()

        payload = {
            "success": True,
            "optimized_consumptions": optimized_consumptions,
            "real_consumptions": real_consumptions,
        }

    except Exception as error:
        db.session.rollback()
        payload = {"success": False, "errors": [str(error)]}

    return payload


def create_consumptions(_obj, info, data):
    # Permits are based on the module name, which is unique on the db. We use the file name as equivalence to the
    # module we are retrieving from db
    module_name = os.path.basename(__file__)[:-3]

    try:
        user = get_user_from_token(request=info.context)
        if user is not None:
            # Fields that are mandatory to create a new device
            is_user_allowed = check_if_user_is_allowed(
                role=user.role, permit=CREATE, module_name=module_name
            )

            if not is_user_allowed:
                raise UserNotAllowed(
                    details="User does not have enough permissions to perform the action requested"
                )

            desired_keys = {"device_id", "consumptions"}

            data_has_desired_keys = verify_dict_has_desired_keys(
                base_dict=data, desired_keys=desired_keys
            )

            if not data_has_desired_keys:
                raise WrongData(
                    details="Some necessary fields are missing from the request's data"
                )

            is_consumptions_valid = (
                isinstance(data.get("consumptions"), list)
                and len(data.get("consumptions")) > 0
            )

            if not is_consumptions_valid:
                raise WrongData(details="Consumptions field sent is not valid")

            device = handle_get_instance_from_user(
                user=user,
                data=data,
                id_from_record=data.get("device_id"),
                desired_keys=desired_keys,
                model=Device,
                module_name="device",
            )

            consumptions = []

            for consumption_data in data.get("consumptions"):
                consumption_data["device"] = device
                consumption = Consumption(fields_map=consumption_data)
                db.session.add(consumption)
                consumptions.append(consumption)

            db.session.commit()
            payload = {"consumptions": consumptions, "success": True}
        else:
            db.session.rollback()
            raise UserNotFound()

    except Exception as error:
        payload = {"success": False, "errors": [str(error)]}

    return payload
