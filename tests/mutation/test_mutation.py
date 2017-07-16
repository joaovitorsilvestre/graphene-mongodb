def test_gen_mutation(mock_person):
    import inspect
    import graphene
    from graphene.utils.str_converters import to_snake_case

    from graphene_mongo.mutation import gen_mutation
    from graphene_mongo.model import ModelSchema

    model_schema = ModelSchema(mock_person, None, mock_person._fields)

    result = gen_mutation(mock_person, model_schema.schema, model_schema.operators_mutation,
                          model_schema.fields_mutation, None)

    assert issubclass(result, graphene.Mutation)
    assert hasattr(result, 'mutate')

    assert result._meta.name == 'Create' + mock_person.__name__
    assert result._meta.local_fields[to_snake_case(mock_person.__name__)]
    assert result._meta.fields[to_snake_case(mock_person.__name__)]

    operators_mutation = inspect.signature(result.__dict__['Field']).parameters['args'].default

    assert operators_mutation == model_schema.operators_mutation


def test_gen_mutation_user_mutation_func(mock_person):
    import graphene
    from graphene_mongo.mutation import gen_mutation
    from graphene_mongo.model import ModelSchema

    def mutate(args, context):
        u = mock_person(**args)
        u.save()
        return u

    model_schema = ModelSchema(mock_person, mutate, mock_person._fields)

    user_mutate_func = gen_mutation(mock_person, model_schema.schema, model_schema.operators_mutation,
                          model_schema.fields_mutation, mutate)

    assert issubclass(user_mutate_func, graphene.Mutation)
    assert hasattr(user_mutate_func, 'mutate')
    assert getattr(user_mutate_func, 'mutate').__name__ == 'user_mutate'
