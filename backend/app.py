import os
from dotenv import load_dotenv
from api import *
from api import models
from api.models.role import Role
from api.models.device import Device
from api.models.consumption import Consumption
from api.models.user import User
from api.models.module import Module
from api.models.authorization import Authorization
from api.resolvers.user import sign_up
from ariadne import graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from api.schema import schema
from datetime import datetime
from ariadne.validation import cost_validator
from api.const import ALL_PERMITS

load_dotenv()

DEV = "DEV"
APP_MODE = os.getenv("APP_MODE")
BASIC_USER = os.getenv("BASIC_USER")
MANAGER_ROLE = os.getenv("MANAGER_ROLE")
DEFAULT = "DEFAULT"
MAXIMUM_COST = 5

module_module_data = {
    "name": "module",
}

authorization_module_data = {"name": "authorization"}

device_module_data = {"name": "device"}

consumption_module_data = {"name": "consumption"}


def give_all_permissions_to_module(module, role):
    for PERMIT in ALL_PERMITS:
        authorization = Authorization(
            fields_map={"module": module, "role": role, "permit": PERMIT}
        )

        db.session.add(authorization)

    db.session.commit()


if APP_MODE == "DEV" or APP_MODE == "DEV_WITH_AUTH":
    db.drop_all()
    db.create_all()
    creation_date = datetime.today().date()
    manager_role = Role(name=MANAGER_ROLE, creation_date=creation_date, default=DEFAULT)

    module_module = Module(fields_map=module_module_data)
    authorization_module = Module(fields_map=authorization_module_data)
    device_module = Module(fields_map=device_module_data)
    consumption_module = Module(fields_map=consumption_module_data)

    db.session.add(manager_role)
    db.session.add(module_module)
    db.session.add(device_module)
    db.session.add(authorization_module)
    db.session.add(consumption_module)
    db.session.commit()

    give_all_permissions_to_module(role=manager_role, module=module_module)
    give_all_permissions_to_module(role=manager_role, module=authorization_module)
    give_all_permissions_to_module(role=manager_role, module=device_module)
    give_all_permissions_to_module(role=manager_role, module=consumption_module)

    sign_up(
        None,
        None,
        {"name": "Blanca Nydia Pérez", "password": "12341234", "email": "bnydiap@gmail.com"},
    )

    # user = User.query.all()[0]
    # device_data = {
    #     "name": "Calefactor",
    #     "user": user,
    #     "min_c": 8,
    #     "average_consumption": 14,
    #     "max_c": 20,
    #     "freq_time": 0.43,
    #     "turn_off": False,
    #     "sort": "U",
    #     "metering": 3,
    # }

    # heater_device = Device(fields_map=device_data)

    # consumption_data = {
    #     "device": heater_device,
    #     "consumption_amount": 1190.78,
    #     "consumption_datetime": datetime(2021, 12, 3, 15, 0, 0),
    # }

    # sample_consumption = Consumption(fields_map=consumption_data)

    # db.session.add(heater_device)
    # db.session.add(sample_consumption)
    db.session.commit()


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        # validation_rules=[cost_validator(MAXIMUM_COST)],
        context_value=request,
        debug=app.debug,
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code
