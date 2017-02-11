from mongoengine import *
import graphene
from graphene.types.datetime import DateTime
from .custom_types import CustomDictField
from .utils import Resolvers


class MongraphSchema(type):
    def __new__(cls, class_name, parents, attrs):
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

    def auto_resolver(self, root, args, contex, info):
        """ this function will be passed to generated subclass """
        return Resolvers.generic_resolver(self, args, info)

    def auto_resolver_list(self, root, args, context, info):
        """ this function will be passed to generated subclass """
        return Resolvers.generic_resolver_list(self, args, info)

    RESPECTIVE_FIELDS = {
        StringField: graphene.String(),
        BooleanField: graphene.Boolean(),
        IntField: graphene.Int(),
        FloatField: graphene.Float(),
        DateTimeField: DateTime(),
        ObjectIdField: graphene.ID(),
        URLField: graphene.String(),
        DictField: CustomDictField()
    }

    SPECIAL_FIELDS = [ReferenceField, ListField, PointField]

    @classmethod
    def convert_fields(cls, schema_attrs, model_attrs, references):
        """ Convert each field of MongoEngine Document to the respective field of Graphene """

        for f_name, mongo_field in model_attrs.items():

            field = None

            if type(mongo_field) not in cls.SPECIAL_FIELDS:
                ''' If the field doesn't need any special treatment '''
                field = cls.RESPECTIVE_FIELDS[type(mongo_field)]

                # That is used as an easy way to pass this Schema fields as second parameter to graphene.Field
                # For instance, graphene.Field(UserSchema, **UserSchema.fields, resolver ...
                schema_attrs['fields'][f_name] = field

            elif type(mongo_field) == ReferenceField:
                schema = references.get(f_name)
                field = graphene.Field(schema, **schema.fields, resolver=schema.auto_resolver)

            elif type(mongo_field) == ListField:
                ''' List Field can be of simple fields, lick String, but it also can be of special fields '''
                list_items_type = type(mongo_field.field)

                if list_items_type not in cls.SPECIAL_FIELDS:
                    # this is necessary because of graphene.List must receive a class not a instance
                    field = graphene.List(type(cls.RESPECTIVE_FIELDS[list_items_type]))
                else:
                    #TODO Here the code is assuming that if the type of list is special, it's everytime referenceField
                    #TODO but it can be another special field, as instance, PointField. Need to Fix that !!!

                    schema = references.get(f_name)
                    field = graphene.List(schema, **schema.fields, resolver=schema.auto_resolver_list)

            elif type(mongo_field) == PointField:
                ''' MongoEngine already treat to the PointField be a list of two items '''
                field = graphene.List(graphene.Float)

            schema_attrs[f_name] = field

        return schema_attrs
