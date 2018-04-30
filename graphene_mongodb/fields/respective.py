import graphene
from graphene.types.datetime import DateTime
from mongoengine import StringField, BooleanField, IntField, FloatField, DateTimeField, ObjectIdField, URLField, \
    DictField, EmailField, LongField, DecimalField, BinaryField, PointField, ReferenceField, ListField, SortedListField

from graphene_mongodb.fields.custom_fields import GenericField, CustomBinaryField, CustomDecimalField
from graphene_mongodb.fields.special_fields import reference_field, list_field


# http://docs.mongoengine.org/guide/defining-documents.html?highlight=emailfield#fields
respective_fields = {
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

respective_special_fields = {
    ReferenceField: reference_field,
    ListField: list_field,
    SortedListField: list_field
}


def field_to_id(m_field, g_field):
    """ We need this because if we want to do a query using the id, we will pass a string to args with the id of the 
    document that we want, but graphene needs a ID field, instead of Field. This function convert to right thing."""

    if isinstance(m_field, ReferenceField):
        return graphene.ID()
    elif (isinstance(m_field, ListField) or isinstance(m_field, SortedListField)) and \
            isinstance(m_field.field, ReferenceField):
        """ Pass here if it is a ListField or SortedListField of ReferenceField """
        return graphene.List(graphene.ID)
    else:
        return g_field
