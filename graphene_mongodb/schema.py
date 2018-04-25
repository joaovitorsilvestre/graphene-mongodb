from six import with_metaclass
from graphene_mongodb.model import ModelSchema
from graphene_mongodb.options import Options


class MongoSchemaMeta(type):
    def __new__(cls, *args):
        class_name, parents, attrs = args

        if not parents:
            return type.__new__(cls, class_name, parents, attrs)

        options = Options(class_name, attrs)
        generated_schema = cls._gen_schema(options.model, options)
        options.single = generated_schema.single
        options.list = generated_schema.list

        return type(class_name, (), dict(generated_schema.to_attrs(), _meta=options))

    _generated_schemas = {}

    @classmethod
    def _gen_schema(cls, model, options=None):
        """ This function is responsible for generate the graphene schema and memoize it """
        options = Options(model.__name__ + 'Schema', {'model': model}) if not options else options

        MongoSchemaMeta._generated_schemas.update({
            model: ModelSchema(model, options.mongo_fields, options.mutate, options.validator)
        })
        return MongoSchemaMeta._generated_schemas[model]

    @classmethod
    def get_or_generate_schema(cls, model):
        if model not in cls._generated_schemas:
            return cls._gen_schema(model)
        else:
            return cls._generated_schemas.get(model)


class MongoSchema(with_metaclass(MongoSchemaMeta)):
    def __new__(cls, model):
        return type(model.__name__ + 'Schema', (MongoSchema,), {'model': model})

