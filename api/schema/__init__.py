from ariadne import load_schema_from_path, make_executable_schema, snake_case_fallback_resolvers
from api.resolvers import query, mutation, datetime_scalar

types = load_schema_from_path('./api/schema/types/')

schema = make_executable_schema(types, query, mutation, datetime_scalar, snake_case_fallback_resolvers)
