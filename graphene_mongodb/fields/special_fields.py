import graphene


def reference_field(f_name, mongo_field):
    """ Generate a schema for RefereceField, or get a schema already done saved in _generated_schemas """
    from graphene_mongodb import MongoSchema

    document = mongo_field.document_type_obj  # document that this ReferenceField references

    schema = MongoSchema.get_or_generate_schema(document).schema
    return graphene.Field(schema)


def list_field(f_name, mongo_field):
    from graphene_mongodb import MongoSchema
    from graphene_mongodb.fields.respective import respective_fields

    list_items_type = type(mongo_field.field)

    if list_items_type in respective_fields:
        return graphene.List(type(respective_fields[list_items_type]()))
    else:
        try:
            document = mongo_field.field.document_type
        except AttributeError:
            raise AttributeError('Error in {} field, have sure that this is defined with a mongoengine field'
                                 .format(f_name))

        schema = MongoSchema.get_or_generate_schema(document).schema
        return graphene.List(schema)
