from six import with_metaclass
from mongoengine import StringField, ReferenceField, Document
import graphene

from .custom_fields import RESPECTIVE_FIELDS, RESPECTIVE_SPECIAL_FIELDS, GenericField, CustomDecimalField, \
    CustomBinaryField, SpecialFields
from .utils import generic_resolver


class MongraphSchemaMeta(type):
    def __new__(cls, class_name, parents, attrs):

        if not parents:
            return type.__new__(cls, class_name, parents, attrs)

        MODEL = attrs.get('__MODEL__')
        cls.verify(class_name, attrs)

        model_attrs = {k: v for k, v in MODEL._fields.items()}  # key: fields name, value: type of mongoField

        attrs.update(cls.convert_fields(model_attrs))           # Fields that appear in paramters (with operators)
        attrs['single'] = classmethod(cls.single)
        attrs['list'] = classmethod(cls.list)

        # here we generate the graphene class and memoize it
        graphene_object_class = type(class_name, (graphene.ObjectType,), attrs)
        cls._generated_schemas[MODEL] = graphene_object_class

        return graphene_object_class

    _generated_schemas = {}  # Store schemas of Documents already generated (Memoization)

    # http://docs.mongoengine.org/guide/querying.html#query-operators
    _OPERATORS = {
        'in': lambda field: graphene.List(type(field)),
        'nin': lambda field: graphene.List(type(field)),
        'gte': lambda field: graphene.String(),
        'lte': lambda field: graphene.String(),
    }

    # http://docs.mongoengine.org/guide/querying.html#string-queries
    _STRING_OPERATORS = ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith',
                        'endswith', 'iendswith', 'match']

    def single(self):
        """ auto generate the graphene field """

        def auto_resolver(root, args, contex, info):
            return generic_resolver(self, args, info)

        return graphene.Field(self, **self.fields, resolver=auto_resolver)

    def list(self):
        """ auto generate the graphene List """
        def auto_resolver_list(root, args, context, info):
            return generic_resolver(self, args, info, is_list=True)

        return graphene.List(self, **self.fields, resolver=auto_resolver_list)

    @classmethod
    def convert_fields(cls, model_attrs):
        result = {'fields': {}}

        for f_name, mongo_field in model_attrs.items():
            field = cls.to_respective(f_name, mongo_field)
            result[f_name] = field
            result['fields'].update(cls.add_operators(f_name, mongo_field, field))

        return result

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
            result[f_name] = graphene.String()
            for op_name in cls._OPERATORS:
                result[f_name + '__' + op_name] = graphene.List(graphene.String)

        return result

    @classmethod
    def verify(cls, class_name, attrs):
        MODEL = attrs.get('__MODEL__')

        if not MODEL:
            raise AttributeError('Failed to generate schema {} '
                                 ', __MODEL__ attribute was not given.'.format(class_name))

        if not issubclass(MODEL, Document):
            raise TypeError('Failed to generate schema {} '
                            ', __MODEL__ must be a subclass of mongoengine.Document.'.format(class_name))


class MongraphSchema(with_metaclass(MongraphSchemaMeta)):
    pass
