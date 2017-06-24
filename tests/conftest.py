import pytest
import graphene
import random
from mongoengine.connection import connect, disconnect


@pytest.yield_fixture(scope="function")
def mongo():
    db_name = str(random.randint(0, 5000000000000000000))
    connection = connect(db=db_name)
    yield
    connection.drop_database(db_name)
    disconnect()


@pytest.fixture(scope='function')
def schema_builder():
    def build(schemas):
        attrs = {schema.__name__.replace('Schema', '').lower(): schema.single() for schema in schemas}
        Query = type('Query', (graphene.ObjectType,), attrs)
        return graphene.Schema(query=Query)
    return build


from tests.mocks import *