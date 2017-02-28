from graphene.types import Scalar
from graphene import Field, List, Boolean


class GenericField(Scalar):
    @staticmethod
    def serialize(_info):
        return _info


class CustomDecimalField(Scalar):
    @staticmethod
    def serialize(_decimal):
        return float(_decimal)


class CustomBinaryField(Scalar):
    @staticmethod
    def serialize(_binary):
        return _binary.decode('utf-8')


class SpecialFields:
    ''' This fields will be called with the same arguments for simplify logic in to_respective function '''

    @staticmethod
    def reference_field(f_name, mongo_field, RESPECTIVE_FIELDS, document=None):
        ''' Generate a schema for RefereceField, or get a schema already done saved in _generated_schemas '''

        from MongographQL import MongraphSchema

        if not document:
            document = mongo_field.document_type_obj

        if hasattr(document, 'parent'):
            ''' Avoid recursion, for instance, a Document has a ReferenceField('self'), when generate
                a schema, it'll do it infinitly '''

            #TODO find a way to generate a schema for ReferenceField('self') without has a maximum recursion
            return Field(Boolean)

        if document not in MongraphSchema._generated_schemas:
            ''' Memoize generated schema '''

            schema = type(f_name, (MongraphSchema,), {
                '__MODEL__': document
            })
            MongraphSchema._generated_schemas.update({
                document: schema
            })
        else:
            schema = MongraphSchema._generated_schemas.get(document)

        return Field(schema, resolver=schema.auto_resolver, **schema.fields)

    @staticmethod
    def list_field(f_name, mongo_field, RESPECTIVE_FIELDS):
        list_items_type = type(mongo_field.field)

        if list_items_type in RESPECTIVE_FIELDS:
            return List(type(RESPECTIVE_FIELDS[list_items_type]()))
        else:
            return SpecialFields.reference_field(f_name,
                                                 mongo_field,
                                                 RESPECTIVE_FIELDS,
                                                 document=mongo_field.field.document_type)
