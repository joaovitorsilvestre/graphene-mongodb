import pytest

from graphene_mongo.options import Options


def test_options_no_model():
    with pytest.raises(Exception) as e_info:
        Options('TestSchema', {})

    assert str(e_info.value) == 'Failed to generate schema {}, model attribute was not given.'.format('TestSchema')


def test_not_mongoengine_document():
    with pytest.raises(Exception) as e_info:
        Options('TestSchema', {'model': False})

    assert str(e_info.value) == 'Failed to generate schema {}, model must be ' \
                                'a subclass of mongoengine.Document.'.format('TestSchema')


def test_mutate_not_static():
    from mongoengine import Document

    class Test(Document):
        pass

    with pytest.raises(Exception) as e_info:
        Options('TestSchema', {'model': Test, 'mutate': 'To fails'})

    assert str(e_info.value) == 'Failed to generate schema {}, mutate method must ' \
                                'be a method with the decorator staticmethod.'.format('TestSchema')


def test_mutate_wrong_number_arguments():
    from mongoengine import Document

    class Test(Document):
        pass

    def mutate():
        pass

    with pytest.raises(Exception) as e_info:
        Options('TestSchema', {'model': Test, 'mutate': staticmethod(mutate)})

    assert str(e_info.value) == 'Failed to generate schema {}, mutate method must accept two params. ' \
                                'The first is the arguments passed to mutate in query, for instance: ' \
                                'username:"NewObjName". Second is the context of the application, if it is flask, ' \
                                'will be flask global request.'.format('TestSchema')


def test_mongoengine_list_of_field_field_not_implemented():
    from graphene_mongo.operators import list_fields
    from mongoengine import FileField, Document

    for list_type in list_fields:
        class Test(Document):
            field_error = list_type(FileField())

        with pytest.raises(Exception) as e_info:
            Options('TestSchema', {'model': Test})

        assert str(e_info.value) == "It was not possible to generate schema for {} because the " \
                                    "field {} is a List of the type {}, and that field is not supported yet."\
                                    .format("Test", 'field_error', type(Test.field_error.field))


def test_mongoengine_field_not_implemented():
    from mongoengine import FileField, Document

    class Test(Document):
        field_error = FileField()

    with pytest.raises(Exception) as e_info:
        Options('TestSchema', {'model': Test})

    assert str(e_info.value) == "It was not possible to generate schema for {} because the " \
                                "field {} is of the type {}, and that field is not supported yet." \
                                .format("Test", 'field_error', FileField)


def test_mongoengine_field_references_self():
    from mongoengine import Document, ReferenceField

    class Test(Document):
        parent = ReferenceField('self')

    with pytest.raises(Exception) as e_info:
        Options('TestSchema', {'model': Test})

    assert str(e_info.value) == "It was not possible to generate schema for {} because the field {} is a " \
                                "ReferenceField to self and this is not supported yet."\
                                .format("TestSchema", 'parent')


def test_validator_wrong():
    from mongoengine import Document, StringField

    class Test(Document):
        parent = StringField()

    with pytest.raises(Exception) as e_info:
        Options('TestSchema', {'model': Test, 'validator': True})

    assert str(e_info.value) == "'validator' attribute must be callable."

    with pytest.raises(Exception) as e_info:
        Options('TestSchema', {'model': Test, 'validator': lambda x: x})

    assert str(e_info.value) == ("The 'validator' attribute must be a callable that accepts four arguments: "
                                 "model, fields, query, special_params. \n"
                                 "model:            mongoengine.Document that the opration is to be made, \n"
                                 "fields:           list of fields that was requested, \n"
                                 "query:            dict with the query parameters, \n"
                                 "special_params:   dict with params used to improve query, as 'limit' and 'skip'")
