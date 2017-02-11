import re

from graphql.utils.ast_to_dict import ast_to_dict
from mongoengine import *
import graphene
from graphene.types.datetime import DateTime

class Utils:
    @staticmethod
    def with_metaclass(*args, **kwargs):
        from six import with_metaclass as six_with_metaclass
        return six_with_metaclass(*args, **kwargs)

    @staticmethod
    def convert_camel_case(string):
        res = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', res).lower()

    @staticmethod
    def generic_resolver_list(grapheneObject, args, info):
        mongoObject = grapheneObject.__MODEL__

        fields = [k for k, v in Utils.get_fields(info).items() if k[:2] != '__']
        results = mongoObject.objects(**args).only(*fields)

        if results:
            def get_user_attrs(u):
                return {f: getattr(u, f) for f in fields}

            return [grapheneObject(**get_user_attrs(u)) for u in results]
        else:
            return []

    @staticmethod
    def parse_field(field):
        """ parse if the field returned by the query is a dict, PointField has that behavior """
        if isinstance(field, dict):
            if 'coordinates' in field:
                return field['coordinates']
        return field

    @staticmethod
    def generic_resolver(grapheneObject, args, info):
        mongoObject = grapheneObject.__MODEL__

        fields = [k for k, v in Utils.get_fields(info).items() if k[:2] != '__']
        fields = [Utils.convert_camel_case(f) for f in fields]

        result = mongoObject.objects(**args).only(*fields).first()

        if result:
            a = {f: getattr(result, f) for f in fields}
            a = {k: Utils.parse_field(v) for k, v in a.items()}

            return grapheneObject(**a)
        else:
            return None

    # author: mixxorz
    @staticmethod
    def collect_fields(node, fragments):
        field = {}

        if node.get('selection_set'):
            for leaf in node['selection_set']['selections']:
                if leaf['kind'] == 'Field':
                    field.update({
                        leaf['name']['value']: Utils.collect_fields(leaf, fragments)
                    })
                elif leaf['kind'] == 'FragmentSpread':
                    field.update(Utils.collect_fields(fragments[leaf['name']['value']],
                                                fragments))

        return field

    # author: mixxorz
    @staticmethod
    def get_fields(info):
        """A convenience function to call collect_fields with info
        Args:
            info (ResolveInfo)
        Returns:
            dict: Returned from collect_fields
        """

        fragments = {}
        node = ast_to_dict(info.field_asts[0])

        for name, value in info.fragments.items():
            fragments[name] = ast_to_dict(value)

        return Utils.collect_fields(node, fragments)

class MongraphSchema(type):
    def __new__(cls, class_name, parents, attrs):
        MODEL = attrs.get('__MODEL__')
        REF = attrs.get('__REF__') or {}

        model_attrs = {k: v for k, v in MODEL._fields.items()}   # key: fields name, value: type of mongoField
        references = {k: v for k, v in REF.items()}                           # key: name of field, value: Schema

        ## this is used to easy way to pass this Schema fields as second paramter to graphene.Field
        # For instance, graphene.Field(UserSchema, **UserSchema.fields, resolver ...
        attrs['fields'] = {}

        attrs = cls.convert_fields(attrs, model_attrs, references) # all fields converted to respective graphene

        # generate the graphene class
        subclass = type(class_name, (graphene.ObjectType,), attrs)

        setattr(subclass, 'resolve_self', classmethod(cls.resolver_self))
        setattr(subclass, 'resolver_self_list', classmethod(cls.resolver_self_list))

        return subclass

    def resolver_self(self, root, args, contex, info):
        """ this function will be passed to generated subclass """
        return Utils.generic_resolver(self, args, info)

    def resolver_self_list(self, root, args, context, info):
        """ this function will be passed to generated subclass """
        return Utils.generic_resolver_list(self, args, info)

    @staticmethod
    def respective_fields():
        return {
            StringField: graphene.String(),
            BooleanField: graphene.Boolean(),
            IntField: graphene.Int(),
            FloatField: graphene.Float(),
            DateTimeField: DateTime(),
            ObjectIdField: graphene.ID(),
            URLField: graphene.String()
        }

    @classmethod
    def is_special_field(cls, mongo_field):
        special_fields = [ReferenceField, ListField, PointField]
        return mongo_field in special_fields

    @classmethod
    def convert_fields(cls, attrs, model_attrs, references):
        for f_name, mongo_field in model_attrs.items():
            if not cls.is_special_field(type(mongo_field)):
                respective_field = cls.respective_fields()[type(mongo_field)]

                attrs[f_name] = respective_field
                attrs['fields'][f_name] = respective_field
            elif type(mongo_field) == ReferenceField:
                Schema = references.get(f_name)
                attrs[f_name] = graphene.Field(Schema, **Schema.fields, resolver=Schema.resolve_self)
            elif type(mongo_field) == ListField:
                # need to resolve type that this list has
                list_type = type(mongo_field.field)

                if not cls.is_special_field(list_type):
                    # this is necessary because of graphene.List must receive a class not a instance
                    respective_field = type(cls.respective_fields()[list_type])
                    attrs[f_name] = graphene.List(respective_field)
                else:
                    Schema = references.get(f_name)
                    attrs[f_name] = graphene.List(Schema, **Schema.fields, resolver=Schema.resolver_self_list)
            elif type(mongo_field) == PointField:
                attrs[f_name] = graphene.List(graphene.Float)

        return attrs

