import iso8601
from graphql.utils.ast_to_dict import ast_to_dict


def parse_operators(args):
    """ Avoid problem that mongoengine for some reason the operators 
        gte, gt, lt, lte doesn't work with dates in isoformat 
    """

    args = {k: v for k, v in args.items() if k not in ['skip', 'limit']}
    for k, v in args.items():
        try:
            is_data = iso8601.parse_date(v)
        except:
            is_data = False

        if is_data:
            args[k] = is_data if is_data else v

    return args


def mongo_to_graphene(mongo_obj, graphene_obj, fields):
    """ Pass fields from mongoengine object to graphene """
    return graphene_obj(**{f: getattr(mongo_obj, f) for f in fields})


# author: mixxorz
def collect_fields(node, fragments):
    field = {}

    if node.get('selection_set'):
        for leaf in node['selection_set']['selections']:
            if leaf['kind'] == 'Field':
                field.update({
                    leaf['name']['value']: collect_fields(leaf, fragments)
                })
            elif leaf['kind'] == 'FragmentSpread':
                field.update(collect_fields(fragments[leaf['name']['value']], fragments))

    return field


# author: mixxorz
def get_fields(info):
    fragments = {}
    node = ast_to_dict(info.field_asts[0])

    for name, value in info.fragments.items():
        fragments[name] = ast_to_dict(value)

    return collect_fields(node, fragments)