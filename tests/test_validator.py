from graphene_mongodb import MongoSchema


def test_validator_raises_error_query(mock_person, schema_builder):
    def verify_permission(model, fields, query, special_params):
        if 'name' in fields:
            raise Exception('Unauthorized Access')

    class PersonSchema(MongoSchema):
        model = mock_person
        validator = verify_permission

    mock_person(name="Test").save()

    schema = schema_builder([(PersonSchema, PersonSchema.single)], [PersonSchema])
    schema.execute("""query testQuery {
        person(name:"Test") {
            name
        }
    }""")


def test_validator_raises_error_mutation(mock_person, schema_builder):
    def verify_permission(model, fields, query, special_params):
        if 'name' in fields:
            raise Exception('Unauthorized Access')

    # tests without user defined mutate
    class PersonSchema(MongoSchema):
        model = mock_person
        validator = verify_permission

    schema = schema_builder([(PersonSchema, PersonSchema.single)], [PersonSchema])

    result = schema.execute("""mutation testMutation {
        createPerson(name:"Test") {
            person {
                name
            }
        }
    }""")

    assert result.errors
    assert str(result.errors[0]) == 'Unauthorized Access'

    # tests with user defined mutate
    class PersonSchema(MongoSchema):
        model = mock_person
        validator = verify_permission

        @staticmethod
        def mutate(args, context):
            u = mock_person(**args)
            u.save()
            return u

    schema = schema_builder([(PersonSchema, PersonSchema.single)], [PersonSchema])

    result = schema.execute("""mutation testMutation {
        createPerson(name:"Test") {
            person {
                name
            }
        }
    }""")

    assert result.errors
    assert str(result.errors[0]) == 'Unauthorized Access'


def test_validator_right_params_types(mock_person, schema_builder):
    def verify_permission(model, fields, query, special_params):
        assert model == mock_person
        assert sorted(fields) == ['id', 'name']
        assert query == {'name__contains': 'Joe'}
        assert special_params == {'skip': 1, 'limit': 2}

    for i in range(5):
        mock_person(name="Joe" + str(i)).save()

    class PersonSchema(MongoSchema):
        model = mock_person
        validator = verify_permission

    schema = schema_builder([(PersonSchema, PersonSchema.list)])
    result = schema.execute(""" query testQuery {
        person(name_Contains: "Joe", skip: 1, limit: 2) {
            id
            name
        }
    }""")

    assert not result.errors
