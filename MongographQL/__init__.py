from six import with_metaclass
from mongoengine import *
import graphene
from graphene.types.datetime import DateTime
from .custom_fields import *
from .utils import Resolvers


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


class MongraphSchemaMeta(type):
    def __new__(cls, class_name, parents, attrs):

        if not parents:
            return type.__new__(cls, class_name, parents, attrs)

        MODEL = attrs.get('__MODEL__')
        REF = attrs.get('__REF__') or {}

        model_attrs = {k: v for k, v in MODEL._fields.items()}   # key: fields name, value: type of mongoField
        references = {k: v for k, v in REF.items()}              # key: name of field, value: Schema
        attrs['fields'] = {}                                     # Shortcut to pass graphene fields

        attrs = cls.convert_fields(attrs, model_attrs, references)  # all fields converted to respective graphene

        # generate the graphene class
        subclass = type(class_name, (graphene.ObjectType,), attrs)

        setattr(subclass, 'auto_resolver', classmethod(cls.auto_resolver))
        setattr(subclass, 'auto_resolver_list', classmethod(cls.auto_resolver_list))

        return subclass

    OPERATORS = {
        'in': lambda field: graphene.List(type(field)),
        'nin': lambda field: graphene.List(type(field)),
    }

    STRING_OPERATORS = ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith',
                        'endswith', 'iendswith', 'match']

    def auto_resolver(self, root, args, contex, info):
        """ this function will be passed to generated subclass """
        return Resolvers.generic_resolver(self, args, info)

    def auto_resolver_list(self, root, args, context, info):
        """ this function will be passed to generated subclass """
        return Resolvers.generic_resolver_list(self, args, info)

    @classmethod
    def convert_fields(cls, schema_attrs, model_attrs, references):
        for f_name, mongo_field in model_attrs.items():
            field = cls.to_respective(f_name, mongo_field, references)
            schema_attrs[f_name] = field
            schema_attrs['fields'].update(cls.add_operators(f_name, mongo_field, field))

        return schema_attrs

    @classmethod
    def add_operators(cls, f_name, mongo_field, field):
        result = {}
        if type(mongo_field) in RESPECTIVE_FIELDS:
            result[f_name] = field

            for op_name, op in cls.OPERATORS.items():
                result[f_name + '__' + op_name] = op(field)

            if type(mongo_field) == StringField:
                for op in cls.STRING_OPERATORS:
                    result[f_name + '__' + op] = graphene.String()

        return result

    @classmethod
    def to_respective(cls, f_name, mongo_field, references):
        if type(mongo_field) in RESPECTIVE_FIELDS:
            return RESPECTIVE_FIELDS[type(mongo_field)]()
        else:
            return RESPECTIVE_SPECIAL_FIELDS[type(mongo_field)](f_name, mongo_field, references, RESPECTIVE_FIELDS)


class MongraphSchema(with_metaclass(MongraphSchemaMeta)):
    pass
