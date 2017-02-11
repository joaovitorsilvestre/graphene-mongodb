from graphql.language import ast
from graphene.types import Scalar


class CustomDictField(Scalar):
    @staticmethod
    def serialize(_dict):
        return _dict
