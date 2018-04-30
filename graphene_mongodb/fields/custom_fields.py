from graphene.types import Scalar
from graphql.language.ast import FloatValue, IntValue


class GenericField(Scalar):
    @staticmethod
    def serialize(_info):
        return _info


class CustomDecimalField(Scalar):
    @staticmethod
    def coerce_float(value):
        try:
            return float(value)
        except ValueError:
            return None

    serialize = coerce_float
    parse_value = coerce_float

    @staticmethod
    def parse_literal(ast):
        if isinstance(ast, (FloatValue, IntValue)):
            return float(ast.value)


class CustomBinaryField(Scalar):
    @staticmethod
    def serialize(_binary):
        return _binary.decode('utf-8')
