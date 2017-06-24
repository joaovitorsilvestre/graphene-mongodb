import graphene
from graphene.types import Scalar
from graphene.types.datetime import DateTime
from mongoengine import StringField, BooleanField, IntField, FloatField, DateTimeField, ObjectIdField, URLField, \
    DictField, EmailField, LongField, DecimalField, BinaryField, PointField, ReferenceField, ListField, SortedListField

from MongographQL.utils import generate_schema


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
    def reference_field(f_name, mongo_field, RESPECTIVE_FIELDS, document=None):
        ''' Generate a schema for RefereceField, or get a schema already done saved in _generated_schemas '''


        if not document:
            document = mongo_field.document_type_obj

        if isinstance(document, str):
            ''' Avoid recursion, for instance, a Document has a ReferenceField('self'), when generate
                a schema, it'll do it infinitly '''

            #TODO find a way to generate a schema for ReferenceField('self') without has a maximum recursion
            return graphene.Field(graphene.Boolean)

        schema = generate_schema(document, f_name)
        return graphene.Field(schema)

    @staticmethod
    def list_field(f_name, mongo_field, RESPECTIVE_FIELDS):
        list_items_type = type(mongo_field.field)

        if list_items_type in RESPECTIVE_FIELDS:
            return graphene.List(type(RESPECTIVE_FIELDS[list_items_type]()))
        else:
            try:
                document = mongo_field.field.document_type
            except AttributeError:
                raise AttributeError('Error in {} field, have sure that this is defined with a mongoengine field'
                                     .format(f_name))

            schema = generate_schema(document, f_name)
            return graphene.List(schema)


RESPECTIVE_FIELDS = {
    StringField: graphene.String,
    BooleanField: graphene.Boolean,
    IntField: graphene.Int,
    FloatField: graphene.Float,
    DateTimeField: DateTime,
    ObjectIdField: graphene.ID,
    URLField: graphene.String,
    DictField: GenericField,
    EmailField: GenericField,
    LongField: GenericField,
    DecimalField: CustomDecimalField,
    BinaryField: CustomBinaryField,
    PointField: GenericField,
}

RESPECTIVE_SPECIAL_FIELDS = {
    ReferenceField: SpecialFields.reference_field,
    ListField: SpecialFields.list_field,
    SortedListField: SpecialFields.list_field
}