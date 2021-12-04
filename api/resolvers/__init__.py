from ariadne import ObjectType, ScalarType
from .user import sign_up, login
from .module import get_modules, upsert_module
from .device import get_devices_from_user, upsert_device
from .datetime import serialize_datetime
from .device import get_devices_from_user
from .consumption import get_optimized_consumptions_from_device, create_consumptions
from .authorization import create_authorizations, get_my_authorizations

datetime_scalar = ScalarType("Datetime")
query = ObjectType("Query")
mutation = ObjectType("Mutation")

datetime_scalar.serializer(serialize_datetime)

mutation_mapper = [
    {"key": "signUp", "function": sign_up},
    {"key": "login", "function": login},
    {"key": "upsertDevice", "function": upsert_device},
    {"key": "createConsumptions", "function": create_consumptions},
    {"key": "createAuthorizations", "function": create_authorizations},
    {"key": "upsertModule", "function": upsert_module},
]

query_mapper = [
    {"key": "getDevicesFromUser", "function": get_devices_from_user},
    {
        "key": "getOptimizedConsumptionsFromDevice",
        "function": get_optimized_consumptions_from_device,
    },
    {"key": "getModules", "function": get_modules},
    {"key": "getMyAuthorizations", "function": get_my_authorizations},
]


def map_to_graphql(mapper, graphql_object):
    for item in mapper:
        graphql_object.set_field(item["key"], item["function"])


map_to_graphql(mapper=mutation_mapper, graphql_object=mutation)
map_to_graphql(mapper=query_mapper, graphql_object=query)
