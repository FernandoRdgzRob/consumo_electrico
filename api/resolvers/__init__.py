from ariadne import ObjectType, ScalarType
from api.resolvers.hitman import get_hitmen
from api.resolvers.user import sign_up, login
from api.resolvers.boss import promote_hitman
from api.resolvers.hit import get_hits, get_hits_assigned_to_me, create_hit
from api.resolvers.datetime import serialize_datetime

datetime_scalar = ScalarType('Datetime')

query = ObjectType('Query')
mutation = ObjectType('Mutation')
query.set_field('getHitmen', get_hitmen)
query.set_field('getHits', get_hits)
query.set_field('getHitsAssignedToMe', get_hits_assigned_to_me)
mutation.set_field('signUp', sign_up)
mutation.set_field('login', login)
mutation.set_field('createHit', create_hit)
mutation.set_field('promoteHitman', promote_hitman)
datetime_scalar.serializer(serialize_datetime)
