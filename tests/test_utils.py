from MongographQL.utils import convert_camel_case, parse_field

def test_convert_camel_case():
    to_test = {
        'username': 'username',
        'testCamelCase': 'test_camel_case',
        '_id': '_id',
        '_lol_': '_lol_'}

    for camel, expect in to_test.items():
        assert convert_camel_case(camel) == expect

def test_parse_field():
    field1 = 'John'
    field2 = {'coordinates': [1, 2]}

    assert parse_field(field1) == field1
    assert parse_field(field2) == [1, 2]
