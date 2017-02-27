from graphql.utils.ast_to_dict import ast_to_dict
from graphene.utils.str_converters import to_snake_case


class Resolvers:
    @staticmethod
    def generic_resolver_list(graphene_object, args, info):
        mongo_object = graphene_object.__MODEL__

        fields = [k for k, v in get_fields(info).items() if k[:2] != '__']
        results = mongo_object.objects(**args).only(*fields)

        if results:
            def get_user_attrs(u):
                return {f: getattr(u, f) for f in fields}

            return [graphene_object(**get_user_attrs(u)) for u in results]
        else:
            return []

    @staticmethod
    def generic_resolver(graphene_object, args, info):
        mongo_object = graphene_object.__MODEL__

        fields = [k for k, v in get_fields(info).items() if k[:2] != '__']
        fields = [to_snake_case(f) for f in fields]

        result = mongo_object.objects(**args).only(*fields).first()

        if result:
            args_with_data = {f: getattr(result, f) for f in fields}
            return graphene_object(**args_with_data)
        else:
            return None


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