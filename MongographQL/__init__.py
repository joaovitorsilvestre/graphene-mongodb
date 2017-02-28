from six import with_metaclass
from mongoengine import StringField, ReferenceField
import graphene

from .custom_fields import RESPECTIVE_FIELDS, RESPECTIVE_SPECIAL_FIELDS, GenericField, CustomDecimalField, \
    CustomBinaryField, SpecialFields
from .utils import generic_resolver


class MongraphSchemaMeta(type):
    def __new__(cls, class_name, parents, attrs):

        if not parents:
            return type.__new__(cls, class_name, parents, attrs)

        MODEL = attrs.get('__MODEL__')

        model_attrs = {k: v for k, v in MODEL._fields.items()}   # key: fields name, value: type of mongoField
        attrs['fields'] = {}                                     # Fields that appear in paramters (with operators)

        attrs = cls.convert_fields(attrs, model_attrs)  # all fields converted to respective graphene

        # generate the graphene class
        graphene_object_class = type(class_name, (graphene.ObjectType,), attrs)

        setattr(graphene_object_class, 'auto_resolver', classmethod(cls.auto_resolver))
        setattr(graphene_object_class, 'auto_resolver_list', classmethod(cls.auto_resolver_list))

        return graphene_object_class

    # Store schemas of Documents already generated (Memoization)
    _generated_schemas = {}

    _OPERATORS = {
        'in': lambda field: graphene.List(type(field)),
        'nin': lambda field: graphene.List(type(field)),
    }

    _STRING_OPERATORS = ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith',
                        'endswith', 'iendswith', 'match']

    def auto_resolver(self, root, args, contex, info):
        """ this function will be passed to generated subclass """
        return generic_resolver(self, args, info)

    def auto_resolver_list(self, root, args, context, info):
        """ this function will be passed to generated subclass """
        return generic_resolver(self, args, info, is_list=True)

    @classmethod
    def convert_fields(cls, schema_attrs, model_attrs):
        for f_name, mongo_field in model_attrs.items():
            field = cls.to_respective(f_name, mongo_field)
            schema_attrs[f_name] = field
            schema_attrs['fields'].update(cls.add_operators(f_name, mongo_field, field))

        return schema_attrs

    @classmethod
    def to_respective(cls, f_name, mongo_field):
        if type(mongo_field) in RESPECTIVE_FIELDS:
            return RESPECTIVE_FIELDS[type(mongo_field)]()
        else:
            return RESPECTIVE_SPECIAL_FIELDS[type(mongo_field)](f_name, mongo_field, RESPECTIVE_FIELDS)

    @classmethod
    def add_operators(cls, f_name, mongo_field, field):
        result = {}
        if type(mongo_field) in RESPECTIVE_FIELDS:
            result[f_name] = field

            for op_name, op in cls._OPERATORS.items():
                result[f_name + '__' + op_name] = op(field)

            if type(mongo_field) == StringField:
                for op in cls._STRING_OPERATORS:
                    result[f_name + '__' + op] = graphene.String()
        elif isinstance(mongo_field, ReferenceField):
            for op_name in cls._OPERATORS:
                result[f_name + '__' + op_name] = graphene.List(graphene.String)

        return result


class MongraphSchema(with_metaclass(MongraphSchemaMeta)):
    pass
