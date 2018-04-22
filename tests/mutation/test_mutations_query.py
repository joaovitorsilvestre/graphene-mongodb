import pytest


def test_gen_mutation_user_mutation_func(schema_builder, mock_person):
    from graphene_mongo import MongoSchema

    assert mock_person.objects().count() == 0

    def mutation_func(args, context):
        PersonSchema._called_custom_mutate = True
        p = mock_person(**args)
        p.save()
        return p

    class PersonSchema(MongoSchema):
        model = mock_person
        mutate = staticmethod(mutation_func)

        _called_custom_mutate = False  # just to test if the user function mutate was called

    schema = schema_builder(mutations=[PersonSchema])
    result = schema.execute("""mutation testMutation {
        createPerson(name:"Test") {
            person {
                name
            }
        }
    }""")

    assert not result.errors
    assert result.data == {'createPerson': {'person': {'name': 'Test'}}}

    assert mock_person.objects().count() == 1
    assert mock_person.objects().first().name == 'Test'
    assert PersonSchema._called_custom_mutate


def test_gen_mutation_generic_mutate(schema_builder, mock_person):
    from graphene_mongo import MongoSchema

    assert mock_person.objects().count() == 0

    class PersonSchema(MongoSchema):
        model = mock_person

    schema = schema_builder(mutations=[PersonSchema])
    result = schema.execute("""mutation testMutation {
        createPerson(name:"Test") {
            person {
                name
            }
        }
    }""")

    assert not result.errors
    assert result.data == {'createPerson': {'person': {'name': 'Test'}}}

    assert mock_person.objects().count() == 1
    assert mock_person.objects().first().name == 'Test'


def test_gen_mutation_user_mutate_wrong_return(mock_person):
    import graphene
    from graphql.execution.base import ResolveInfo

    from graphene_mongo.mutation import gen_mutation
    from graphene_mongo.model import ModelSchema

    def mutate(args, context):
        return False

    model_schema = ModelSchema(mock_person, mock_person._fields, mutate, None)

    result = gen_mutation(mock_person, model_schema.schema, model_schema.operators_mutation,
                          model_schema.fields_mutation, model_schema.mutate_func, None)

    assert issubclass(result, graphene.Mutation)
    assert hasattr(result, 'mutate')

    with pytest.raises(Exception) as e_info:
        context = graphene.types.Context()
        info = ResolveInfo('name', *[None for i in range(8)], context)

        result.mutate(None, info, **{'name': "Test"})

    assert str(e_info.value) == 'Failed to resolve mutation of the schema {}' \
                                ' because mutate function must return a instance of {}, and the return type was {}.'\
                                .format(model_schema.schema.__name__, model_schema.model.__name__, type(False))