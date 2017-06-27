from graphql.utils.ast_to_dict import ast_to_dict
from graphene.utils.str_converters import to_snake_case


def generic_resolver(graphene_object, args, info, is_list=False):
    ''' An generic resolver to auto handle query's and return graphene objects with the data '''

    mongo_doc = graphene_object.__MODEL__

    fields = [k for k, v in get_fields(info).items() if k != '__MODEL__']
    fields = [to_snake_case(f) for f in fields]
    query = {k: v for k, v in args.items() if k not in ['skip', 'limit']}

    if is_list:
        result = mongo_doc.objects(**query).only(*fields)

        ## update the query if there's options in args
        if 'skip' in args:
            result = result.skip(args['skip'])
            
        if 'limit' in args:
            result = result.limit(args['limit'])
    else:
        result = mongo_doc.objects(**query).only(*fields).first()

    if result and is_list:
        def get_document_attrs(doc):
            return {f: getattr(doc, f) for f in fields}

        return [graphene_object(**get_document_attrs(doc)) for doc in result]
    elif result and not is_list:
        args_with_data = {f: getattr(result, f) for f in fields}
        return graphene_object(**args_with_data)
    else:
        return [] if is_list else None


def generate_schema(document, f_name):
    ''' Generate a schema for ReferenceField and memoize it to MongraphSchema
        If the schema already has been generated, it'll will be returned
    '''
    from MongographQL import MongraphSchema

    if document not in MongraphSchema._generated_schemas:
        ''' Generate schema and memoize it '''

        schema = type(f_name, (MongraphSchema,), {
            '__MODEL__': document
        })
        MongraphSchema._generated_schemas.update({
            document: schema
        })
    else:
        schema = MongraphSchema._generated_schemas.get(document)

    return schema


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