from graphene.types import Scalar
from graphene import Field, List


class GenericField(Scalar):
    @staticmethod
    def serialize(_info):
        return _info


class CustomDecimalField(Scalar):
    @staticmethod
    def serialize(_decimal):
        return float(_decimal)


class CustomBinaryField(Scalar):
    @staticmethod
    def serialize(_binary):
        return _binary.decode('utf-8')


class SpecialFields:
    ''' This fields will be called with the same arguments for simplify logic in to_respective function '''

    @staticmethod
    def reference_field(f_name, mongo_field, references, RESPECTIVE_FIELDS):
        schema = references.get(f_name)
        return Field(schema, resolver=schema.auto_resolver, **schema.fields)

    @staticmethod
    def list_field(f_name, mongo_field, references, RESPECTIVE_FIELDS):
        list_items_type = type(mongo_field.field)

        if list_items_type in RESPECTIVE_FIELDS:
            return List(type(RESPECTIVE_FIELDS[list_items_type]()))
        else:
            schema = references.get(f_name)
            return List(schema, resolver=schema.auto_resolver_list, **schema.fields)
