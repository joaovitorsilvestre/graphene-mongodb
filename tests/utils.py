import unittest

from mongoengine import connect
import graphene


MONGO_TEST_DB = 'mongraphqltest'


class MongographQLTestCase(unittest.TestCase):
    def setUp(self):
        self._connection = connect(db=MONGO_TEST_DB)

    def tearDown(self):
        self._connection.drop_database(MONGO_TEST_DB)

    def QueryBuilder(self, fields):
        attrs = {schema.__name__.replace('Schema', '').lower(): graphene.Field(schema, **schema.fields, resolver=schema.auto_resolver)
                 for schema in fields}

        return type('Query', (graphene.ObjectType,), attrs)
