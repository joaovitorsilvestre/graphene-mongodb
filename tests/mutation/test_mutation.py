def test_gen_mutation(mock_person):
    import graphene
    from graphene.utils.str_converters import to_snake_case
    from graphene.types.field import Field

    from graphene_mongo.mutation import gen_mutation
    from graphene_mongo.model import ModelSchema

    model_schema = ModelSchema(mock_person, mock_person._fields, None, None)

    result = gen_mutation(mock_person, model_schema.schema, model_schema.operators_mutation,
                          model_schema.fields_mutation, None, None)

    assert issubclass(result, graphene.Mutation)
    assert hasattr(result, 'mutate')

    assert result._meta.name == 'Create' + mock_person.__name__
    assert isinstance(result._meta.fields[to_snake_case(mock_person.__name__)], Field)

    assert result._meta.arguments == model_schema.operators_mutation


def test_gen_mutation_user_mutation_func(mock_person):
    import graphene
    from graphene_mongo.mutation import gen_mutation
    from graphene_mongo.model import ModelSchema

    def mutate(args, context):
        u = mock_person(**args)
        u.save()
        return u

    model_schema = ModelSchema(mock_person, mock_person._fields, mutate, None)

    user_mutate_func = gen_mutation(mock_person, model_schema.schema, model_schema.operators_mutation,
                          model_schema.fields_mutation, mutate, None)

    assert issubclass(user_mutate_func, graphene.Mutation)
    assert hasattr(user_mutate_func, 'mutate')
    assert getattr(user_mutate_func, 'mutate').__name__ == 'user_mutate'


def test_mutation_fields(mock_person, schema_builder):
    from graphene_mongo import MongoSchema
    from mongoengine import Document, DecimalField

    class Person(Document):
        remember_pi = DecimalField(precision=11, default=None)

    p = Person(remember_pi=3.14159265359)
    p.save()

    class PersonSchema(MongoSchema):
        model = Person

        @staticmethod
        def mutate(args, context):
            u = Person(**args)
            u.save()
            return u

    schema = schema_builder([(PersonSchema, PersonSchema.single)], [PersonSchema])

    result = schema.execute("""mutation testMutation {
      createPerson(rememberPi: 3.14159265359) {
        person {
          rememberPi
        }
      }
    }""")

    assert not result.errors
    assert result.data == {'createPerson': {'person': {'rememberPi': 3.14159265359}}}
