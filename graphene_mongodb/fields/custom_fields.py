from graphene.types import Scalar
from graphql.language.ast import FloatValue, IntValue


class GenericField(Scalar):
    @staticmethod
    def serialize(_info):
        return _info


class CustomDictField(Scalar):
    @staticmethod
    def serialize(_info):
        return _info

    @staticmethod
    def parse_dict(ast):
        if not ast.fields:
            return {}

        final_dict = {}
        for item in ast.fields:
            key, value = item.name.value, item.value.value
            final_dict[key] = value

        return final_dict

    parse_value = parse_dict
    parse_literal = parse_dict


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

    @staticmethod
    def parse_binary(ast):
        try:
            return str(ast.value).encode('utf-8')
        except ValueError:
            return None

    parse_value = parse_binary
    parse_literal = parse_binary
