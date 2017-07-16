from graphene.types import Scalar


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