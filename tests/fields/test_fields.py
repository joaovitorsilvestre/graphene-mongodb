import pytest


def test_list_field_no_field():
    """ Assert that raises error if a ListField is given without a type, for instance: ListField() """
    from graphene_mongo.fields.special_fields import list_field
    from mongoengine import ListField

    with pytest.raises(Exception) as e_info:
        list_field('test_field', ListField())

    assert str(e_info.value) == str(AttributeError('Error in {} field, have sure that this is defined with a '
                                                   'mongoengine field'.format('test_field')))
