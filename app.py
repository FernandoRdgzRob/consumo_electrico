import os
from dotenv import load_dotenv
from api import *
from api import models
from api.models.role import Role
from api.resolvers.user import sign_up
from ariadne import graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from api.schema import schema
from datetime import datetime
from ariadne.validation import cost_validator

load_dotenv()

DEV = "DEV"
APP_MODE = os.getenv("APP_MODE")
DEFAULT = "DEFAULT"
MANAGER_ROLE = os.getenv("MANAGER_ROLE")
HITMAN_ROLE = os.getenv("HITMAN_ROLE")
BOSS_ROLE = os.getenv("BOSS_ROLE")
MAXIMUM_COST = 5

if APP_MODE == DEV:
    db.drop_all()
    db.create_all()
    creation_date = datetime.today().date()
    hitman_role = Role(name=HITMAN_ROLE, creation_date=creation_date, default=DEFAULT)
    manager_role = Role(name=MANAGER_ROLE, creation_date=creation_date)
    boss_role = Role(name=BOSS_ROLE, creation_date=creation_date)
    db.session.add(hitman_role)
    db.session.add(manager_role)
    db.session.add(boss_role)
    db.session.commit()

    sign_up(
        None,
        None,
        {
            "name": "Diego Flores",
            "password": "12345",
            "email": "diegoflores@gmail.com"
        }
    )


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        validation_rules=[cost_validator(MAXIMUM_COST)],
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code
