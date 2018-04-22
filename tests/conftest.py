import pytest
import graphene
import random
from mongoengine.connection import connect, disconnect


@pytest.yield_fixture(scope="function")
def mongo():
    db_name = str(random.randint(0, 5000000000000000000))
    connection = connect(db=db_name, host="mongomock://localhost")
    yield
    connection.drop_database(db_name)
    disconnect()


@pytest.fixture(scope='function')
def schema_builder():
    def build(schemas=None, mutations=None):
        Query = None
        Mutation = None

        if schemas:
            attrs = {schema[0].model.__name__.lower(): schema[1] for schema in schemas}
            Query = type('Query', (graphene.ObjectType,), attrs)

        if mutations:
            attrs = {'create_' + m.model.__name__.lower(): m.mutate for m in mutations}
            Mutation = type('Mutation', (graphene.ObjectType,), attrs)

        return graphene.Schema(query=Query, mutation=Mutation)

    return build


from tests.mocks import *
