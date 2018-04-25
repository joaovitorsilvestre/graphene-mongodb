from collections.abc import Sequence
import inspect
from mongoengine import Document
from graphene_mongodb.operators import list_fields, reference_fields
from graphene_mongodb.fields.respective import respective_fields, respective_special_fields


class Options:
    """ This class makes all necessary verifications of types that was given by user """

    def __init__(self, class_name, attrs):
        self.class_name = class_name
        self.model, self.mutate, self.mongo_fields, self.validator = self.verified_attrs(attrs)

    def verified_attrs(self, attrs):
        """ Function to verify if the attributes is of the right type """
        model = attrs.get('model')
        mutate = attrs.get('mutate')
        validator = attrs.get('validator')
        validator = validator.__func__ if isinstance(validator, staticmethod) else validator

        if model is None:
            raise AttributeError('Failed to generate schema {},'
                                 ' model attribute was not given.'.format(self.class_name))

        if not model or not issubclass(model, Document):
            raise TypeError('Failed to generate schema {}, model must be '
                            'a subclass of mongoengine.Document.'.format(self.class_name))

        if mutate and not isinstance(mutate, staticmethod):
            raise TypeError('Failed to generate schema {}, mutate method must '
                            'be a method with the decorator staticmethod.'.format(self.class_name))

        if mutate and len(inspect.signature(mutate.__func__).parameters) != 2:
            raise TypeError('Failed to generate schema {}, mutate method must accept two params. '
                            'The first is the arguments passed to mutate in query, for instance: username:"NewObjName".'
                            ' Second is the context of the application, if it is flask, will be flask global request.'
                            .format(self.class_name))

        # verify if all fields of document is supported
        for f_name, m_field in model._fields.items():
            if type(m_field) not in respective_fields and type(m_field) not in respective_special_fields:
                raise NotImplementedError("It was not possible to generate schema for {} because the "
                                          "field {} is of the type {}, and that field is not supported yet."
                                          .format(model.__name__, f_name, type(m_field)))

            if isinstance(m_field, list_fields):
                if type(m_field.field) not in respective_fields and type(m_field.field) not in respective_special_fields:
                    raise NotImplementedError("It was not possible to generate schema for {} because the "
                                              "field {} is a List of the type {}, and that field is not supported yet."
                                              .format(model.__name__, f_name, type(m_field.field)))

            if isinstance(m_field, reference_fields):
                if isinstance(m_field.document_type_obj, str) and m_field.document_type_obj == 'self':
                    raise NotImplementedError("It was not possible to generate schema for {} because the "
                                              "field {} is a ReferenceField to self and this is not supported yet."
                                              .format(self.class_name, f_name))

        if validator and not callable(validator):
            raise AttributeError("'validator' attribute must be callable.")
        elif validator and len(inspect.signature(validator).parameters) != 4:
            raise AttributeError("The 'validator' attribute must be a callable that accepts four arguments: "
                                 "model, fields, query, special_params")

        return model, mutate.__func__ if mutate else None, model._fields, validator
