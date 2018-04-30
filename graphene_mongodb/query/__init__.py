from graphene.utils.str_converters import to_snake_case
from graphene_mongodb.query.utils import get_fields, parse_operators, mongo_to_graphene


# Options that we can pass as operators to define the query
special_query_parameters = ['skip', 'limit']


def do_query(m_object, query, fields, special_params, is_list):
    query = m_object.objects(**query).only(*fields)

    if 'skip' in special_params:
        query = query.skip(special_params['skip'])
    if 'limit' in special_params:
        query = query.limit(special_params['limit'])

    return query


def resolver_query(g_object, m_object, args, info, is_list=False, validator=None):
    fields = [to_snake_case(f) for f in get_fields(info)]
    query = parse_operators(args)
    special_params = {k: v for k, v in args.items() if k in ['skip', 'limit']}

    if validator:
        validator(m_object, fields, query, special_params)

    result = do_query(m_object, query, fields, special_params, is_list)

    if result and is_list:
        return [mongo_to_graphene(obj, g_object, fields) for obj in result]
    elif result:
        return mongo_to_graphene(result.first(), g_object, fields)
    else:
        return [] if is_list else None
