import graphene
from mongoengine import ObjectIdField

from graphene_mongodb.query import special_query_parameters
from graphene_mongodb.operators import gen_operators_of_field, allowed_operators
from graphene_mongodb.fields.respective import respective_special_fields, respective_fields, field_to_id


def convert_fields(attrs_mongo_doc):
    """ Return a tuple od dicts,
    @param attrs_mongo_doc: dict of attributes of the mongoengine.Document, that is accessible by Document._fields     
    fields: is the pure fields, key is the name of field, and values is the repective graphene field
    fields_mutation: is the fields that is used in mutation, that will go direct in args of mutation
    operators_mutation: is the fields that user set values to be saved on document
    operators_single: is the fields with operators that will be in the query for a single result
    operators_list: same of operators single, but these are avaliable only for query of lists
    """

    fields, fields_mutation, operators_mutation, operators_single = {}, {}, {}, {}

    for f_name, mongo_field in attrs_mongo_doc.items():
        field = RelationMongoGraphene(name=f_name, mongo_field=mongo_field)

        fields[f_name] = field.graphene
        operators_single.update(field.operators)
        fields_mutation[f_name] = field.mutation
        if not isinstance(mongo_field, ObjectIdField):
            operators_mutation[f_name] = field.mutation

    operators_list = operators_single.copy()
    operators_single['skip'] = graphene.Int()

    operators_list.update({p: graphene.Int() for p in special_query_parameters})

    return fields, fields_mutation, operators_mutation, operators_single, operators_list


class RelationMongoGraphene:
    """ Abstraction of Relation between mongoengine field and graphene field """

    def __init__(self, name, mongo_field):
        self.name = name
        self.mongo = mongo_field
        self.graphene = RelationMongoGraphene.to_respective_graphene(name, mongo_field)

        self.mutation = field_to_id(self.mongo, self.graphene)
        self.operators = gen_operators_of_field(self.name, self.mongo, self.graphene, allowed_operators(self.mongo))

    @staticmethod
    def to_respective_graphene(f_name, mongo_field):
        """ Function that given field, returns the respective field of graphene """
        t_mongo_field = type(mongo_field)

        if t_mongo_field in respective_fields:
            return respective_fields[t_mongo_field]()
        else:
            return respective_special_fields[t_mongo_field](f_name, mongo_field)
