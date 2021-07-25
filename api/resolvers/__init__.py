from ariadne import ObjectType, ScalarType
from api.resolvers.hitman import get_hitmen
from api.resolvers.user import sign_up, login
from .datetime import serialize_datetime

datetime_scalar = ScalarType('Datetime')

query = ObjectType('Query')
mutation = ObjectType('Mutation')
query.set_field('getHitmen', get_hitmen)
mutation.set_field('signUp', sign_up)
mutation.set_field('login', login)
datetime_scalar.serializer(serialize_datetime)
