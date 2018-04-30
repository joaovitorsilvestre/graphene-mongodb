import graphene
from graphene.utils.str_converters import to_snake_case

from graphene_mongodb.query import mongo_to_graphene


def gen_mutation(model, graphene_schema, operators_mutation, fields_mutation, mutate_func, validator):
    """ We need to create a class that seems as follows (http://docs.graphene-python.org/en/latest/types/mutations/):

    class CreatePerson(graphene.Mutation):
        class Input:
            name = graphene.String()
    
        ok = graphene.Boolean()
        person = graphene.Field(lambda: Person)
    
        @staticmethod
        def mutate(root, args, context, info):
            person = Person(name=args.get('name'))
            ok = True
            return CreatePerson(person=person, ok=ok) 
    """

    def user_mutate(root, info, **kwargs):
        if validator:
            validator(model, kwargs, {}, {})

        obj = mutate_func(kwargs, info.context)
        if not isinstance(obj, model):
            raise TypeError('Failed to resolve mutation of the schema {}'
                            ' because mutate function must return a instance of {}, and the return type was {}.'
                            .format(graphene_schema.__name__, model.__name__, type(obj)))

        graphene_obj = mongo_to_graphene(obj, graphene_schema, fields_mutation)
        return Create(**{to_snake_case(model.__name__): graphene_obj})

    def generic_mutate(root, info, **kwargs):
        if validator:
            validator(model, kwargs, {}, {})

        obj = model(**kwargs)
        obj.save()
        graphene_obj = mongo_to_graphene(obj, graphene_schema, fields_mutation)
        return Create(**{to_snake_case(model.__name__): graphene_obj})

    Create = type('Create' + model.__name__, (graphene.Mutation,), {
        'Arguments': type('Arguments', (), operators_mutation),
        to_snake_case(model.__name__): graphene.Field(lambda: graphene_schema),
        'mutate': staticmethod(generic_mutate) if not mutate_func else staticmethod(user_mutate)
    })

    return Create
