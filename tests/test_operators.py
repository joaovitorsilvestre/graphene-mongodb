from tests.utils import MongographQLTestCase
from mongoengine import *

from MongographQL import MongraphSchema
import graphene


class OperatorsTest(MongographQLTestCase):
    def test_in(self):
        """ Tests the operator's 'in' and 'nin' """

        class Person(Document):
            name = StringField()

        class PersonSchema(MongraphSchema):
            __MODEL__ = Person

        Person(name="John").save()

        Query = self.QueryBuilder([PersonSchema])
        schema = graphene.Schema(query=Query)

        # operator in
        result = schema.execute(""" query testQuery {
           person(name_In: ["Travolta"]) {
               name
           }
        }""")
        assert result.data == {'person': None}

        result = schema.execute(""" query testQuery {
           person(name_In: ["John"]) {
               name
           }
        }""")
        assert result.data == {'person': {'name': 'John'}}

        # operator nin
        result = schema.execute(""" query testQuery {
           person(name_Nin: ["John"]) {
               name
           }
        }""")
        assert result.data == {'person': None}

        result = schema.execute(""" query testQuery {
           person(name_Nin: ["Travolta"]) {
               name
           }
        }""")
        assert result.data == {'person': {'name': 'John'}}


class StringOperatorsTest(MongographQLTestCase):
    def test_exact(self):
        """ Tests the operator's 'exact' and 'iexact' """

        class Person(Document):
            name = StringField()

        class PersonSchema(MongraphSchema):
            __MODEL__ = Person

        Person(name="John").save()

        Query = self.QueryBuilder([PersonSchema])
        schema = graphene.Schema(query=Query)

        # operator 'exact', case sensitive
        result = schema.execute(""" query testQuery {
           person(name_Exact: "john") {
               name
           }
        }""")
        assert result.data == {'person': None}

        result = schema.execute(""" query testQuery {
           person(name_Exact: "John") {
               name
           }
        }""")
        assert result.data == {'person': {'name': 'John'}}

        # operator 'iexact', case insensitive
        result = schema.execute(""" query testQuery {
           person(name_Iexact: "travolta") {
               name
           }
        }""")
        assert result.data == {'person': None}

        result = schema.execute(""" query testQuery {
           person(name_Iexact: "John") {
               name
           }
        }""")
        assert result.data == {'person': {'name': 'John'}}

        result = schema.execute(""" query testQuery {
           person(name_Iexact: "john") {
               name
           }
        }""")
        assert result.data == {'person': {'name': 'John'}}

    def test_contains(self):
        """ Tests the operator's 'contains' and 'icontains' """
        class Person(Document):
            name = StringField()

        class PersonSchema(MongraphSchema):
            __MODEL__ = Person

        Person(name="John").save()

        Query = self.QueryBuilder([PersonSchema])
        schema = graphene.Schema(query=Query)

        # operator 'contains', case sensitive
        result = schema.execute(""" query testQuery {
           person(name_Contains: "john") {
               name
           }
        }""")
        assert result.data == {'person': None}

        result = schema.execute(""" query testQuery {
           person(name_Contains: "John") {
               name
           }
        }""")
        assert result.data == {'person': {'name': 'John'}}

        # operator 'icontains', case insensitive
        result = schema.execute(""" query testQuery {
           person(name_Icontains: "john") {
               name
           }
        }""")
        assert result.data == {'person': {'name': 'John'}}

        result = schema.execute(""" query testQuery {
           person(name_Icontains: "John") {
               name
           }
        }""")
        assert result.data == {'person': {'name': 'John'}}

    def test_startswith(self):
        """ Tests the operator's 'startswith' and 'istartswith' """
        class Person(Document):
            name = StringField()

        class PersonSchema(MongraphSchema):
            __MODEL__ = Person

        Person(name="John").save()

        Query = self.QueryBuilder([PersonSchema])
        schema = graphene.Schema(query=Query)

        # operator 'startswith', case sensitive
        result = schema.execute(""" query testQuery {
           person(name_Startswith: "j") {
               name
           }
        }""")
        assert result.data == {'person': None}

        result = schema.execute(""" query testQuery {
           person(name_Startswith: "J") {
               name
           }
        }""")
        assert result.data == {'person': {'name': 'John'}}

        # operator 'istartswith', case insensitive
        result = schema.execute(""" query testQuery {
           person(name_Istartswith: "j") {
               name
           }
        }""")
        assert result.data == {'person': {'name': 'John'}}

        result = schema.execute(""" query testQuery {
           person(name_Istartswith: "J") {
               name
           }
        }""")
        assert result.data == {'person': {'name': 'John'}}

    def test_endswith(self):
        """ Tests the operator's 'endswith' and 'iendswith' """
        class Person(Document):
            name = StringField()

        class PersonSchema(MongraphSchema):
            __MODEL__ = Person

        Person(name="JOHN").save()

        Query = self.QueryBuilder([PersonSchema])
        schema = graphene.Schema(query=Query)

        # operator 'endswith', case sensitive
        result = schema.execute(""" query testQuery {
           person(name_Endswith: "n") {
               name
           }
        }""")
        assert result.data == {'person': None}

        result = schema.execute(""" query testQuery {
           person(name_Endswith: "N") {
               name
           }
        }""")
        assert result.data == {'person': {'name': 'JOHN'}}

        # operator 'iendswith', case insensitive
        result = schema.execute(""" query testQuery {
           person(name_Iendswith: "n") {
               name
           }
        }""")
        assert result.data == {'person': {'name': 'JOHN'}}

        result = schema.execute(""" query testQuery {
           person(name_Iendswith: "N") {
               name
           }
        }""")
        assert result.data == {'person': {'name': 'JOHN'}}
