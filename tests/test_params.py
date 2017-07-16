from graphene_mongo import MongoSchema


def test_skip_parameter(schema_builder, mock_person):
    """ without operator we consider that is a string with an id """
    persons = [mock_person(name=str(i)) for i in range(10)]
    for p in persons:
        p.save()

    PersonSchemaList = MongoSchema(mock_person)

    schema = schema_builder([(PersonSchemaList, PersonSchemaList.list)])
    result = schema.execute(""" query testQuery {
        person(skip: 5) {
            name
        }
    }""")

    assert isinstance(result.data['person'], list)
    assert len(result.data['person']) == 5
    for i, person in enumerate(result.data['person']):
        assert person['name'] == persons[i+5].name


def test_limit_parameter(schema_builder, mock_person):
    """ without operator we consider that is a string with an id """
    persons = [mock_person(name=str(i)) for i in range(10)]
    for p in persons:
        p.save()

    PersonSchemaList = MongoSchema(mock_person)

    schema = schema_builder([(PersonSchemaList, PersonSchemaList.list)])
    result = schema.execute(""" query testQuery {
        person(limit: 5) {
            name
        }
    }""")

    assert isinstance(result.data['person'], list)
    assert len(result.data['person']) == 5
    for i, person in enumerate(result.data['person']):
        assert person['name'] == persons[i].name