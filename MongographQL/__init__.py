from graphql.utils.ast_to_dict import ast_to_dict
from mongoengine import *
import graphene

class Utils:
    @staticmethod
    def with_metaclass(*args, **kwargs):
        from six import with_metaclass as six_with_metaclass
        return six_with_metaclass(*args, **kwargs)

    @staticmethod
    def generic_resolver(grapheneObject, args, info):
        mongoObject = grapheneObject.__MODEL__

        fields = [k for k, v in Utils.get_fields(info).items() if k[:2] != '__']
        result = mongoObject.objects(**args).only(*fields).first()

        if result:
            a = {f: getattr(result, f) for f in fields}
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

        model_attrs = {k: type(v) for k, v in MODEL._fields.items() if k != 'id'}   # key: fields name, value: type of mongoField
        references = {k: v for k, v in REF.items()}                                 # key: name of field, value: Schema

        ## this is used to easy way to pass this Schema fields as second paramter to graphene.Field
        # For instance, graphene.Field(UserSchema, **UserSchema.fields, resolver ...
        attrs['fields'] = {}

        attrs = cls.convert_fields(attrs, model_attrs, references) # all fields converted to respective graphene

        # generate the graphene class
        subclass = type(class_name, (graphene.ObjectType,), attrs)

        setattr(subclass, 'resolve_self', classmethod(cls.resolver_self))

        return subclass

    def resolver_self(self, root, args, contex, info):
        """ this function will be passed to generated subclass """
        return Utils.generic_resolver(self, args, info)

    @staticmethod
    def respective_fields():
        return {
            StringField: graphene.String(),
            BooleanField: graphene.Boolean(),
            IntField: graphene.Int(),
            FloatField: graphene.Float(),
        }

    @classmethod
    def respective_special_field(cls, f_name, mongo_field, references):
        if mongo_field == ReferenceField:
            Schema = references.get(f_name)
            return graphene.Field(Schema, **Schema.fields, resolver=Schema.resolve_self)

    @classmethod
    def is_special_field(cls, mongo_field):
        return mongo_field == ReferenceField

    @classmethod
    def convert_fields(cls, attrs, model_attrs, references):
        for f_name, mongo_field in model_attrs.items():
            if not cls.is_special_field(mongo_field):
                respective_field = cls.respective_fields()[mongo_field]

                attrs[f_name] = respective_field
                attrs['fields'][f_name] = respective_field
            else:
                attrs[f_name] = cls.respective_special_field(f_name, mongo_field, references)

        return attrs

