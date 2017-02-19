from graphql.language import ast
from graphene.types import Scalar


class CustomDictField(Scalar):
    @staticmethod
    def serialize(_dict):
        return _dict


class CustomEmailField(Scalar):
    @staticmethod
    def serialize(_email):
        return _email


class CustomLongField(Scalar):
    @staticmethod
    def serialize(_longInt):
        return _longInt


class CustomDecimalField(Scalar):
    @staticmethod
    def serialize(_decimal):
        return float(_decimal)


class CustpmBinaryField(Scalar):
    @staticmethod
    def serialize(_binary):
        return _binary.decode('utf-8')

