from app import db
from .authorization import check_if_user_is_allowed
from .basic_logic import (
    verify_dict_doesnt_have_unaccepted_keys,
    verify_dict_has_desired_keys,
)
from ...exceptions.bad_request import WrongData
from ...exceptions.not_allowed import UserNotAllowed
from ...const import CREATE, UPDATE, READ


def handle_create_instance(
    user, module_name: str, data: dict, model, desired_keys: set
):
    is_user_allowed = check_if_user_is_allowed(
        role=user.role, permit=CREATE, module_name=module_name
    )

    if not is_user_allowed:
        raise UserNotAllowed()

    dict_has_desired_keys = verify_dict_has_desired_keys(
        base_dict=data, desired_keys=desired_keys
    )

    if not dict_has_desired_keys:
        raise WrongData()

    instance = model(fields_map=data)

    db.session.add(instance)

    db.session.commit()

    return instance


def handle_update_instance(
    user, module_name: str, data: dict, model, accepted_keys: set, id_from_record, id_key
):
    is_user_allowed = check_if_user_is_allowed(
        role=user.role, permit=UPDATE, module_name=module_name
    )

    if not is_user_allowed:
        raise UserNotAllowed()

    dict_has_desired_keys = verify_dict_doesnt_have_unaccepted_keys(
        base_dict=data, accepted_keys=accepted_keys
    )

    if not dict_has_desired_keys:
        raise WrongData()

    instance = model.query.filter_by(id=id_from_record)

    if instance.first() is None:
        raise WrongData(details=f"The record with id {id_from_record} does not exist")

    del data[id_key]

    instance.update(data)

    db.session.commit()

    return instance.first()


def handle_get_all_instances(user, module_name: str, model):
    is_user_allowed = check_if_user_is_allowed(
        role=user.role, permit=READ, module_name=module_name
    )

    if not is_user_allowed:
        raise UserNotAllowed()

    instances = model.query.all()

    return instances


def handle_get_instance_from_user(
    user, data, id_from_record, desired_keys, model, module_name
):
    is_user_allowed = check_if_user_is_allowed(
        role=user.role, permit=READ, module_name=module_name
    )

    if not is_user_allowed:
        raise UserNotAllowed()

    data_has_desired_keys = verify_dict_has_desired_keys(
        base_dict=data, desired_keys=desired_keys
    )

    if not data_has_desired_keys:
        raise WrongData(
            details="Some necessary fields are missing from the request's data"
        )

    record = model.query.get(id_from_record)

    if record is None:
        raise WrongData(details="Record requested does not exist")

    if record.user != user:
        raise UserNotAllowed(details="User does not fulfill necessary permissions")

    return record
