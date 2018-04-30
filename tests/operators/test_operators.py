import graphene


def format_fields(fields):
    return sorted(['test__' + f for f in fields] + ['test'])


def test_add_operators_to_field_respective_fields():
    from graphene_mongodb.fields.respective import respective_fields
    from graphene_mongodb.operators import gen_operators_of_field, string_operators, allowed_operators, \
                                         fields_string_operators

    for m_field, r_graphene in respective_fields.items():
        m_field = m_field()
        applied_operators = gen_operators_of_field('test', m_field, r_graphene, allowed_operators(m_field))

        expected = set(format_fields(allowed_operators(m_field)) + \
                   (format_fields(string_operators) if isinstance(m_field, fields_string_operators) else []))

        assert len(applied_operators.keys()) == len(expected)
        assert sorted(list(applied_operators.keys())) == sorted(expected)


def test_add_operators_to_field_list_field():
    from mongoengine import ListField, SortedListField
    from graphene_mongodb.operators import gen_operators_of_field, allowed_operators
    from graphene_mongodb.fields.respective import respective_special_fields, respective_fields

    for m_field in [ListField, SortedListField]:
        for f, r_graphene in respective_fields.items():
            field = m_field(f())

            applied_operators = gen_operators_of_field('test', field, respective_special_fields[m_field],
                                                       allowed_operators(field))

            expected = format_fields(['size'])

            assert len(applied_operators.keys()) == len(expected)
            assert sorted(list(applied_operators.keys())) == sorted(expected)

            obj_list_field = applied_operators['test']('listTest', field)
            assert isinstance(obj_list_field, graphene.List)

            # here we test to assert that the type of items of the list is what is suppose to be
            assert isinstance(obj_list_field.of_type, type(r_graphene))


def test_add_operators_to_field_reference_field():
    from mongoengine import ReferenceField, Document, StringField
    from graphene_mongodb.operators import gen_operators_of_field, allowed_operators
    from graphene_mongodb.fields import respective_special_fields

    class Other(Document):
        name = StringField()

    class Test(Document):
        test = ReferenceField(Other)

    field = Test.test
    r_graphene = respective_special_fields[type(field)]
    applied_operators = gen_operators_of_field('test', field, r_graphene('test', field), allowed_operators(field))

    assert sorted(list(applied_operators.keys())) == format_fields(['in', 'nin', 'ne'])

    assert isinstance(applied_operators['test__in'], graphene.List)
    assert isinstance(applied_operators['test__nin'], graphene.List)
    assert isinstance(applied_operators['test__ne'], graphene.ID)
