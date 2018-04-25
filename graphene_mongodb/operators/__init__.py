import graphene
from mongoengine import IntField, FloatField, DateTimeField, LongField, DecimalField, BooleanField, ObjectIdField, \
                        DictField, BinaryField, PointField, ListField, SortedListField, ReferenceField, StringField, \
                        URLField, EmailField
from graphene_mongodb.fields.respective import field_to_id

# http://docs.mongoengine.org/guide/querying.html#query-operators
operators = {
    'ne': lambda m_field, g_field:  field_to_id(m_field, g_field),
    'lt': lambda m_field, g_field:  field_to_id(m_field, g_field),
    'lte': lambda m_field, g_field: field_to_id(m_field, g_field),
    'gt': lambda m_field, g_field:  field_to_id(m_field, g_field),
    'gte': lambda m_field, g_field: field_to_id(m_field, g_field),
    'in': lambda m_field, g_field:  graphene.List(type(field_to_id(m_field, g_field))),
    'nin': lambda m_field, g_field: graphene.List(type(field_to_id(m_field, g_field))),
    'exists': lambda _, __:         graphene.Boolean(),
    'size': lambda _, __:           graphene.Int()
}

# http://docs.mongoengine.org/guide/querying.html#string-queries
string_operators = ['exact', 'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith']

fields_string_operators = (StringField, URLField, EmailField)
reference_fields = (ReferenceField,)
scalar_fields = (IntField, FloatField, DateTimeField, LongField, DecimalField)
specific_fields = (BooleanField, ObjectIdField, DictField, BinaryField, PointField)
list_fields = (ListField, SortedListField)


def allowed_operators(mongo_field):
    if isinstance(mongo_field, fields_string_operators) or isinstance(mongo_field, scalar_fields):
        return list(operators.keys())
    elif isinstance(mongo_field, specific_fields):
        return ['ne', 'in', 'nin', 'exists']
    elif isinstance(mongo_field, reference_fields):
        return ['in', 'nin', 'ne']
    elif isinstance(mongo_field, list_fields):
        return ['size']


def gen_operators_of_field(f_name, mongo_field, r_graphene, operators_list):
    """ Return a dict with keys as the name of the field with operator and value is the required type, for instance: 
    @param f_name: string name of the field
    @param mongo_field: object instance of mongoengine field, e.g: mongoengine.StringField()
    @param r_graphene: object instance of graphene field, e.g: graphene.String(): 
    {
        name: graphene.String()
        name__nin: graphene.List(graphene.String) ...
    }
     """

    field_with_operators = {
        f_name: field_to_id(mongo_field, r_graphene)
    }

    for op_name in operators_list:
        field_with_operators[f_name + '__' + op_name] = operators[op_name](mongo_field, r_graphene)

    if isinstance(mongo_field, fields_string_operators):
        for op in string_operators:
            field_with_operators[f_name + '__' + op] = graphene.String()

    return field_with_operators
