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
        """Recursively collects fields from the AST
        Args:
            node (dict): A node in the AST
            fragments (dict): Fragment definitions
        Returns:
            A dict mapping each field found, along with their sub fields.
            {'name': {},
             'sentimentsPerLanguage': {'id': {},
                                       'name': {},
                                       'totalSentiments': {}},
             'slug': {}}
        """

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
        model = attrs.get('__MODEL__')
        model_attrs = {k: v for k, v in model._fields.items() if k != 'id'}

        dict_convert = {
            StringField: graphene.String(),
            BooleanField: graphene.Boolean(),
            IntField: graphene.Int(),
            FloatField: graphene.Float(),
        }

        ## attr to store the type for use it in graphene.Field(... username=graphene.String etc
        attrs['fields'] = {}

        for k, v in model_attrs.items():
            respective_graphene = dict_convert.get(type(v))

            attrs[k] = respective_graphene
            attrs['fields'][k] = respective_graphene

        subclass = type(class_name, (graphene.ObjectType,), attrs)

        #add the resolver
        setattr(subclass, 'resolve_self', classmethod(cls.resolver_self))

        return subclass

    def resolver_self(self, root, args, contex, info):
        return Utils.generic_resolver(self, args, info)