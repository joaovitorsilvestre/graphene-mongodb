import graphene

from graphene_mongodb.fields import convert_fields
from graphene_mongodb.query import resolver_query
from graphene_mongodb.mutation import gen_mutation


class ModelSchema:
    def __init__(self, model, attrs_mongo_doc, mutate, validator):
        self.model = model
        self.mutate_func = mutate  # mutate function that user specified
        self.validator = validator

        self.fields, self.fields_mutation, self.operators_mutation,\
            self.operators_single, self.operators_list = convert_fields(attrs_mongo_doc)

        self.schema = type(self.model.__name__ + 'Graphene', (graphene.ObjectType,), self.fields.copy())

    def to_attrs(self):
        return {
            'single': self.single(),
            'list': self.list(),
            'fields': self.fields,
            'model': self.model,
            'mutate': self.mutate().Field()
        }

    def mutate(self):
        return gen_mutation(self.model, self.schema, self.operators_mutation, self.fields_mutation, self.mutate_func,
                            self.validator)

    def single(self):
        return ModelSchema.resolver(self.schema, self.model, operators_single=self.operators_single,
                                    validator=self.validator)

    def list(self):
        return ModelSchema.resolver(self.schema, self.model, operators_list=self.operators_list,
                                    validator=self.validator, is_list=True)

    @staticmethod
    def resolver(g_schema, mongo_doc, operators_single=None, operators_list=None, is_list=False, validator=None):
        def auto_resolver(root, info, **kwargs):
            return resolver_query(g_schema, mongo_doc, kwargs, info, is_list=is_list, validator=validator)

        if is_list:
            return graphene.List(g_schema, **operators_list, resolver=auto_resolver)
        else:
            return graphene.Field(g_schema, **operators_single, resolver=auto_resolver)
